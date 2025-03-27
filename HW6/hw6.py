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