# HW6 - Recommendation Systems
### Ethan Novak
### CS 432, Spring 2025
### Sunday April 6, 2025 11:59pm

# Script

I edited the provided script to answer the questions. The script can be found in a file named `hw6.py` in this repository, and I also pasted it below. The script is a movie recommendation system using collaborative filtering and demographic similarity.  The script has been modified to output the required information to answer questions one, two, and three. For question 1, the script displays the demographics and movie ratings of the most similar users based on demographics. For question 2, the script shows the top 5 most and least correlated users based on the Pearson correlation. And, for question 3, the script lists the top and bottom 5 recommended movies for the current user. 

```
import os
import sys
from math import sqrt

def sim_pearson(prefs, p1, p2):
    '''
    Returns a distance-based similarity score for person1 and person2.
    '''

    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    
    if len(si) == 0:
        return 0
    
    n = len(si)

    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    
    if den == 0:
        return 0
    
    return num / den

def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) 
              for other in prefs if other != person]
    
    scores.sort(reverse=True)
    return scores[0:n]

def getRecommendations(prefs, person, similarity=sim_pearson):
    '''
    Gets recommendations for a person by using a weighted average
    of every other user's rankings
    '''
    
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        
        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                simSums.setdefault(item, 0)
                simSums[item] += sim
    
    rankings = [(total / simSums[item], item) for (item, total) in totals.items()]
    
    rankings.sort(reverse=True)
    return rankings

def load_users(path):
    users = {}
    try:
        with open(os.path.join(path, 'u.user'), 'r') as f:
            for line in f:
                user_id, age, gender, occupation, zipcode = line.strip().split('|')
                users[user_id] = {
                    'age': int(age),
                    'gender': gender,
                    'occupation': occupation
                }
    except FileNotFoundError:
        print(f"Error: Could not find u.user file in {path}")
        sys.exit(1)
    
    return users

def load_movies(path):
    movies = {}
    try:
        with open(os.path.join(path, 'u.item'), 'r', encoding='latin-1') as f:
            for line in f:
                parts = line.strip().split('|')
                movie_id, movie_title = parts[0], parts[1]
                movies[movie_id] = movie_title
    except FileNotFoundError:
        print(f"Error: Could not find u.item file in {path}")
        sys.exit(1)
    
    return movies

def load_ratings(path, movies):
    ratings = {}
    try:
        with open(os.path.join(path, 'u.data'), 'r') as f:
            for line in f:
                user_id, movie_id, rating, _ = line.strip().split('\t')
                movie_title = movies.get(movie_id, 'Unknown Movie')
                
                if user_id not in ratings:
                    ratings[user_id] = {}
                
                ratings[user_id][movie_title] = float(rating)
    except FileNotFoundError:
        print(f"Error: Could not find u.data file in {path}")
        sys.exit(1)
    
    return ratings

def calculate_demographic_similarity(current_user, user):
    score = 0
    
    age_diff = abs(current_user['age'] - user['age'])
    if age_diff <= 5:
        score += 1
    elif age_diff <= 10:
        score += 0.5
    
    if current_user['gender'] == user['gender']:
        score += 1
    
    if current_user['occupation'] == user['occupation']:
        score += 1
    
    return score

def find_most_similar_users(current_user_data, users, k=3):
    """
    Find k most similar users based on demographics.
    """
    user_similarities = []
    
    for user_id, user_data in users.items():
        similarity = calculate_demographic_similarity(current_user_data, user_data)
        user_similarities.append((user_id, similarity))
    
    user_similarities.sort(key=lambda x: x[1], reverse=True)
    
    return [user_id for user_id, _ in user_similarities[1:k+1]]

def get_top_and_bottom_movies(user_ratings, n=3):
    sorted_ratings = sorted(user_ratings.items(), key=lambda x: x[1], reverse=True)
    
    top_movies = sorted_ratings[:n]
    bottom_movies = sorted_ratings[-n:]
    
    return top_movies, bottom_movies

def main(path='ml-100k'):
    movies = load_movies(path)
    users = load_users(path)
    ratings = load_ratings(path, movies)
    
    current_user_data = {
        'age': 22, 
        'gender': 'M', 
        'occupation': 'student'
    }
    
    similar_user_ids = find_most_similar_users(current_user_data, users)
    
    print("# Q1 Answer")
    for user_id in similar_user_ids:
        print(f"\nUser {user_id} Demographics:")
        print(f"  Age: {users[user_id]['age']}")
        print(f"  Gender: {users[user_id]['gender']}")
        print(f"  Occupation: {users[user_id]['occupation']}")
        
        top_movies, bottom_movies = get_top_and_bottom_movies(ratings[user_id])
        
        print("\n  Top 3 Movies:")
        for movie, rating in top_movies:
            print(f"    {movie}: {rating}")
        
        print("\n  Bottom 3 Movies:")
        for movie, rating in bottom_movies:
            print(f"    {movie}: {rating}")
    
    substitute_user = similar_user_ids[0]
    
    print("\n# Q2 Answer")
    top_correlated = topMatches(ratings, substitute_user)
    print("Top 5 Most Correlated Users:")
    for correlation, user in top_correlated:
        print(f"  User {user}: Correlation {correlation:.3f}")
    
    bottom_correlated = topMatches(ratings, substitute_user, similarity=lambda prefs, p1, p2: -sim_pearson(prefs, p1, p2))
    print("\nBottom 5 Least Correlated Users:")
    for correlation, user in bottom_correlated:
        print(f"  User {user}: Correlation {correlation:.3f}")
    
    print("\n# Q3 Answer")
    recommendations = getRecommendations(ratings, substitute_user)
    
    print("Top 5 Recommended Movies:")
    for rating, movie in recommendations[:5]:
        print(f"  {movie}: Predicted Rating {rating:.2f}")
    
    print("\nBottom 5 Recommended Movies:")
    for rating, movie in recommendations[-5:]:
        print(f"  {movie}: Predicted Rating {rating:.2f}")

if __name__ == '__main__':
    main()
```

# Q1 Answer

The script finds three users most similar to me demodemographically, then it displays their demographics, and finally, it shows the top and bottom three movies for each user. 

For user 37, his top three favorite films are Batman (1989), Pulp Fiction (1994), and Top Gun (1986); his bottom three least favorite films are Dragonheart (1996), Indepdence Day (1996), and Jurassic Park (1993). 

For user 66, his top three favorite films are Return of the Jedi, Courage Under Fire, and Ransom; his bottom three least favorite films are Excess Baggage, Muppet Treasure Island, and The English Patient. 

For user 67, his top three favorite movies are Shawshank Redemption, Beavis and Butt-head Do America, and Mission: Impossible; his bottom three least favorite movies are Father of the Bride Part II, Multiplicity, and Very Brady Sequel.

Out of these three specific users, I guess that I relate most to user 37. I did enjoy the Batman movie and Top Gun, however, I have never seen Pulp Fiction. Additionally, I am not big a fan of Jurassic Park, Independence Day, or Dragonheart.

```
User 37 Demographics:
  Age: 23
  Gender: M
  Occupation: student

  Top 3 Movies:
    Batman (1989): 5.0
    Pulp Fiction (1994): 5.0
    Top Gun (1986): 5.0

  Bottom 3 Movies:
    Dragonheart (1996): 2.0
    Independence Day (ID4) (1996): 2.0
    Jurassic Park (1993): 1.0

User 66 Demographics:
  Age: 23
  Gender: M
  Occupation: student

  Top 3 Movies:
    Return of the Jedi (1983): 5.0
    Courage Under Fire (1996): 5.0
    Ransom (1996): 5.0

  Bottom 3 Movies:
    Excess Baggage (1997): 1.0
    Muppet Treasure Island (1996): 1.0
    English Patient, The (1996): 1.0

User 67 Demographics:
  Age: 17
  Gender: M
  Occupation: student

  Top 3 Movies:
    Shawshank Redemption, The (1994): 5.0
    Beavis and Butt-head Do America (1996): 5.0
    Mission: Impossible (1996): 5.0

  Bottom 3 Movies:
    Father of the Bride Part II (1995): 3.0
    Multiplicity (1996): 3.0
    Very Brady Sequel, A (1996): 1.0
```

# Q2 Answer

After running the script, the output for question two is as follows: 

```
Top 5 Most Correlated Users:
  User 93: Correlation 1.000
  User 937: Correlation 1.000
  User 859: Correlation 1.000
  User 791: Correlation 1.000
  User 754: Correlation 1.000

Bottom 5 Least Correlated Users:
  User 491: Correlation 1.000
  User 80: Correlation 1.000
  User 736: Correlation 1.000
  User 672: Correlation 1.000
  User 641: Correlation 1.000
```

Q: Which 5 users are most correlated to the substitute you (i.e., which 5 users rate movies most similarly to the substitute you?)

A: The five users that are most correlated to the substitue me are user 93, user 937, user 859, user 791, and user 754. 

Q: Which 5 users are least correlated (i.e., negative correlation)?

A: The five users that are least correlated to me are user 491, user 80, user 736, user 672, and user 641. 

Q: Explain the general operation of any functions you use from recommendations.py.

A: The script first imports `os`, `sys` for file handling and `sqrt` from `math` for calculating the square root. The `sim_pearson` function takes three arguments (`prefs`, `p1`, and `p2`), and it finds common items between p1 and p2, it calculates sums of ratings and squared sums and product sums, and it computes the Pearson score based on these sums. The `topMatches` functions finds the top `n` most similar users to a given `person`, and it uses the provided `similarity` function argument to measure similarity. Finally, this function sorts the scores in descending order and returns the top `n` users. The `getRecommendations` function calculates the similarity with the target user, aggregates ratings for movies not already rated by the target user, and returns a sorted list of movie recommendations based on the predicted ratings. The `load_users` function loads user demographic data from a file located at the argument `path`. The `load_movies` function loads movie demographic data from a file located at the argument `path`. The `load_ratings` function does the same, except for rating data. The `calculate_demographic_similarity` function computes a demographic score between two users based on their age, gender, and occupation. The `find_most_similar_users` functions finds the `k` most similar users to the current user based on the demographic data. Finally, the `get_top_and_bottom_movies` function finds the top `n` and bottom `n` movies based on user ratings and sorts the ratings and selects the highest and lowest. 

# Q3 Answer

After running the script, the output for question three is as follows: 

```
Top 5 Recommended Movies:
  They Made Me a Criminal (1939): Predicted Rating 5.00
  Someone Else's America (1995): Predicted Rating 5.00
  Santa with Muscles (1996): Predicted Rating 5.00
  Prefontaine (1997): Predicted Rating 5.00
  Marlene Dietrich: Shadow and Light (1996) : Predicted Rating 5.00

Bottom 5 Recommended Movies:
  Amityville Curse, The (1990): Predicted Rating 1.00
  Amityville 3-D (1983): Predicted Rating 1.00
  Amityville 1992: It's About Time (1992): Predicted Rating 1.00
  American Strays (1996): Predicted Rating 1.00
  3 Ninjas: High Noon At Mega Mountain (1998): Predicted Rating 1.00
```

Q: What are the top 5 recommendations for films that the substitute you should see?

A: The top five reommendations for films that the substitute me should see are They Made Me a Criminal, Someone Else's America, Santa with Muscles, Prefontaine, and Marlene Dietrich: Shadow and Light.

Q: What are the bottom 5 recommendations (i.e., films the substitute you is almost certain to hate)?

A: The bottom five recommendations are Amityville Curse, Amityville 3-D, Amityville 1992: It's About Time, American Strays, and 3 Ninjas: High Noon At Mega Mountain.

Q: Explain the general operation of any functions you use from recommendations.py.

A: The script first imports `os`, `sys` for file handling and `sqrt` from `math` for calculating the square root. The `sim_pearson` function takes three arguments (`prefs`, `p1`, and `p2`), and it finds common items between p1 and p2, it calculates sums of ratings and squared sums and product sums, and it computes the Pearson score based on these sums. The `topMatches` functions finds the top `n` most similar users to a given `person`, and it uses the provided `similarity` function argument to measure similarity. Finally, this function sorts the scores in descending order and returns the top `n` users. The `getRecommendations` function calculates the similarity with the target user, aggregates ratings for movies not already rated by the target user, and returns a sorted list of movie recommendations based on the predicted ratings. The `load_users` function loads user demographic data from a file located at the argument `path`. The `load_movies` function loads movie demographic data from a file located at the argument `path`. The `load_ratings` function does the same, except for rating data. The `calculate_demographic_similarity` function computes a demographic score between two users based on their age, gender, and occupation. The `find_most_similar_users` functions finds the `k` most similar users to the current user based on the demographic data. Finally, the `get_top_and_bottom_movies` function finds the top `n` and bottom `n` movies based on user ratings and sorts the ratings and selects the highest and lowest. 

# Q4 Answer

To answer this question, I chose Toy Story (1995) as my favorite film and Broken English (1996) as my least favorite film. Additionally, I modified the script to correspond with this information. For example, I added the following code to the `main` function: 

```
    target_movie1 = "Toy Story (1995)"
    if target_movie1 in movie_prefs:
        top_corr, bottom_corr = get_movie_correlations(movie_prefs, target_movie1, n=5)
        
        print(f"\nTop 5 Most Correlated Movies to '{target_movie1}':")
        for correlation, movie in top_corr:
            print(f"  {movie}: Correlation {correlation:.3f}")
        
        print(f"\nBottom 5 Least Correlated Movies to '{target_movie1}':")
        for correlation, movie in bottom_corr:
            print(f"  {movie}: Correlation {correlation:.3f}")
    else:
        print(f"Movie '{target_movie1}' not found in the dataset")
    
    target_movie2 = "Broken English (1996)"
    if target_movie2 in movie_prefs:
        top_corr, bottom_corr = get_movie_correlations(movie_prefs, target_movie2, n=5)
        
        print(f"\nTop 5 Most Correlated Movies to '{target_movie2}':")
        for correlation, movie in top_corr:
            print(f"  {movie}: Correlation {correlation:.3f}")
        
        print(f"\nBottom 5 Least Correlated Movies to '{target_movie2}':")
        for correlation, movie in bottom_corr:
            print(f"  {movie}: Correlation {correlation:.3f}")
    else:
        print(f"Movie '{target_movie2}' not found in the dataset")
```

Furthermore, I also created a new function, `get_movie_correlations`, that calculates both the top and bottom correlated movies for a given movie. Below is the function:

```
def get_movie_correlations(movie_prefs, movie_name, n=5):
    top_correlations = topMatches(movie_prefs, movie_name, n=n)
    bottom_correlations = topMatches(movie_prefs, movie_name, n=n, 
                                   similarity=lambda prefs, m1, m2: -sim_pearson(prefs, m1, m2))
    
    return top_correlations, bottom_correlations
```

After running the script, here is the output: 

```
Top 5 Most Correlated Movies to 'Toy Story (1995)':
  Substance of Fire, The (1996): Correlation 1.000
  Ladybird Ladybird (1994): Correlation 1.000
  Infinity (1996): Correlation 1.000
  Phantoms (1998): Correlation 1.000
  Old Lady Who Walked in the Sea, The (Vieille qui marchait dans la mer, La) (1991): Correlation 1.000  

Bottom 5 Least Correlated Movies to 'Toy Story (1995)':
  Winter Guest, The (1997): Correlation 1.000
  Underneath, The (1995): Correlation 1.000
  Stalker (1979): Correlation 1.000
  Slingshot, The (1993): Correlation 1.000
  Schizopolis (1996): Correlation 1.000

Top 5 Most Correlated Movies to 'Broken English (1996)':
  Usual Suspects, The (1995): Correlation 1.000
  Young Poisoner's Handbook, The (1995): Correlation 1.000
  Wizard of Oz, The (1939): Correlation 1.000
  Wishmaster (1997): Correlation 1.000
  Wings of Desire (1987): Correlation 1.000

Bottom 5 Least Correlated Movies to 'Broken English (1996)':
  Terminator, The (1984): Correlation 1.000
  African Queen, The (1951): Correlation 1.000
  While You Were Sleeping (1995): Correlation 1.000
  True Lies (1994): Correlation 1.000
  Top Gun (1986): Correlation 1.000
```

Q: What are the top 5 most correlated films to your favorite film? Bottom 5 least correlated?

A: The top five most correlated films to my favorite film (Toy Story (1995)) are The Substance of Fire (1996), Ladybird Ladybird (1994), Infinity (1996), Phantoms (1998), and The Old Lady Who Walked in the Sea (Vieille qui marchait dans la mer, La) (1991). Furthermore, the bottom five least correlated films are The Winter Guest (1997), The Underneath (1995), Stalker (1979), The Slingshot (1993), and Schizopolis (1996).

Q: What are the top 5 most correlated films to your least favorite film? Bottom 5 least correlated?

A: The top five most correlated films to my least favorite film (Broken English (1996)) are The Usual Suspects, The (1995), The Young Poisoner's Handbook (1995), The Wizard of Oz (1939), Wishmaster (1997), and Wings of Desire (1987). Furthermore, the bottom five least correlated films are The Terminator (1984), African Queen (1951), While You Were Sleeping (1995), True Lies (1994), and Top Gun (1986): Correlation 1.000. 

Q: Based on your knowledge of the resulting films, do you agree with the results? In other words, do you personally like/dislike the resulting films?

A: Yes, I do agree with the results. Concerning Toy Story, after watching the trailers, I believe that I would like the movies that correlate with it. Additionally, I also dislike the movies that correlate with Toy Story the least, such as Stalker, The Slingshot, and The Underneath.  Moreover, concerning the movies that correlate most with Broken English, except for The Wizard of Oz, I do not like any of the movies that correlate with Broken English. I do like the Wizard of Oz, however. Additionally, I like all the movies that correlate least with Broken English, such as The Terminator, The African Queen, While You Were Sleeping, True Lies, and Top Gun.  Therefore, yes, altogether, I would say that I do agree with the results. 

Here are the trailers that I watched:

[Schizopolis Trailer](https://www.youtube.com/watch?v=f2E7ArARdaE)\
[The Old Lady Who Walked in the Sea (Vieille qui marchait dans la mer, La) Trailer](https://www.youtube.com/watch?v=w3r65BYdGh8)\
[Wishmaster Trailer](https://www.youtube.com/watch?v=aJgl3uoxXc0)\
[The Winter Guest Trailer](https://www.youtube.com/watch?v=fnrKwmH_nic)\

Q: Explain the general operation of any functions you use from recommendations.py.

A: The script first imports `os`, `sys` for file handling and `sqrt` from `math` for calculating the square root. The `sim_pearson` function takes three arguments (`prefs`, `p1`, and `p2`), and it finds common items between p1 and p2, it calculates sums of ratings and squared sums and product sums, and it computes the Pearson score based on these sums. The `topMatches` functions finds the top `n` most similar users to a given `person`, and it uses the provided `similarity` function argument to measure similarity. Finally, this function sorts the scores in descending order and returns the top `n` users. The `getRecommendations` function calculates the similarity with the target user, aggregates ratings for movies not already rated by the target user, and returns a sorted list of movie recommendations based on the predicted ratings. The `load_users` function loads user demographic data from a file located at the argument `path`. The `load_movies` function loads movie demographic data from a file located at the argument `path`. The `load_ratings` function does the same, except for rating data. The `calculate_demographic_similarity` function computes a demographic score between two users based on their age, gender, and occupation. The `find_most_similar_users` functions finds the `k` most similar users to the current user based on the demographic data. Finally, the `get_top_and_bottom_movies` function finds the top `n` and bottom `n` movies based on user ratings and sorts the ratings and selects the highest and lowest. 

# References

* Build a Recommendation Engine with Collaborative Filtering, <https://realpython.com/build-recommendation-engine-collaborative-filtering/>
* How to Build a Movie Recommendation System Based on Collaborative Filtering, <https://www.freecodecamp.org/news/how-to-build-a-movie-recommendation-system-based-on-collaborative-filtering/>
* doguilmak - Book Recommendation with Collaborative Filtering, <https://github.com/doguilmak/Book-Recommendation-with-Collaborative-Filtering>
