# HW6 - Recommendation Systems
### Ethan Novak
### CS 432, Spring 2025
### Sunday April 6, 2025 11:59pm

I edited the provided script to answer the questions. The script can be found in a file named `hw6.py` in this repository, and I also pasted it below. The script is a movie recommendation system using collaborative filtering and demographic similarity. The script first imports `os`, `sys` for file handling and `sqrt` from `math` for calculating the square root. The `sim_pearson` function takes three arguments (`prefs`, `p1`, and `p2`), and it finds common items between p1 and p2, it calculates sums of ratings and squared sums and product sums, and it computes the Pearson score based on these sums. The `topMatches` functions finds the top `n` most similar users to a given `person`, and it uses the provided `similarity` function argument to measure similarity. Finally, this function sorts the scores in descending order and returns the top `n` users. The `getRecommendations` function calculates the similarity with the target user, aggregates ratings for movies not already rated by the target user, and returns a sorted list of movie recommendations based on the predicted ratings. The `load_users` function loads user demographic data from a file located at the argument `path`. The `load_movies` function loads movie demographic data from a file located at the argument `path`. The `load_ratings` function does the same, except for rating data. 

The `calculate_demographic_similarity` function computes a demographic score between two users based on their age, gender, and occupation. The `find_most_similar_users` functions finds the `k` most similar users to the current user based on the demographic data. Finally, the `get_top_and_bottom_movies` function finds the top `n` and bottom `n` movies based on user ratings and sorts the ratings and selects the highest and lowest. The script outputs the required information to answer questions one, two, and three. For question 1, the script displays the demographics and movie ratings of the most similar users based on demographics. For question 2, the script shows the top 5 most and least correlated users based on the Pearson correlation. And, for question 3, the script lists the top and bottom 5 recommended movies for the current user. 

# Script
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
# Q3 Answer
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
# Q4 Answer

# References
