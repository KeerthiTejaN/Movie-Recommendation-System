from __future__ import division
import csv
import math

class User_Diction_Values(object):
    def min_max_normalize(self):
        ratings = self.ratings.values()
        average = 0
        for rating in ratings:
            average += rating
        self.average = average/len(self.ratings.values())
        for movie_id in self.ratings:
            self.ratings[movie_id] = self.ratings[movie_id] - self.average

    def rated_movie(self, movie_id):
        return movie_id in self.ratings

    def __init__(self):
        super(User_Diction_Values, self).__init__()
        self.average = None
        self.ratings = {}

class MovieDetails(object):
    def __init__(self):
        super(MovieDetails, self).__init__()
        self.users_dict = {}

def data_tuple(filename):
    data_list = []
    with open(filename,'r') as umr:
        reader = csv.reader(umr,delimiter='\t')
        for data in reader:
            data_list.append([int(r) for r in data[:-1]])
    return data_list

def ten_million(filename):
    data_line = []
    f = open(filename)
    all_lines = f.readlines()
    for each_line in all_lines:
        cut_lines = each_line.split('::')
        cut_lines = map(int,cut_lines)
    data_line.append(cut_lines[:-1])
    return data_line

def users_data(data_list):
    User_diction ={}
    for cell in data_list:
        user_id = cell[0]
        movie_id = cell[1]
        rating = cell[2]
        user_object = None
        if user_id in User_diction:
            user_object = User_diction[user_id]
        else:
            user_object = User_Diction_Values()
            User_diction[user_id] = user_object
        user_object.ratings[movie_id] = rating
    for userid in User_diction:
        User_diction[userid].min_max_normalize()
    return User_diction

def movie_data(user_diction):
    Movie_diction ={}
    for uid in user_diction.keys():
        for mid in user_diction[uid].ratings:
            rating = user_diction[uid].ratings[mid]
            movie_object = None
            if mid in Movie_diction:
                movie_object = Movie_diction[mid]
            else:
                movie_object = MovieDetails()
                Movie_diction[mid] = movie_object
            movie_object.users_dict[uid] = rating

    return Movie_diction

def lmax_distance(user1,user2,user1_age,user2_age,user1_gender,user2_gender):
    both_rated = set(user1.ratings.keys()) & set(user2.ratings.keys())
    if user1_gender == user2_gender:
        gender_value =0
    else :
        gender_value =1
    age_gap = abs(user1_age - user2_age)
    if age_gap < 10:
        age_factor = 0
    elif age_gap > 10 and age_gap < 20:
        age_factor = 0.25
    elif age_gap >= 20 and age_gap < 30:
        age_factor = 0.5
    elif age_gap >= 30 and age_gap < 40 :
        age_factor = 0.75
    else:
        age_factor = 1

    if len(both_rated) == 0:
       return ((0.125*age_factor)+(0.125*gender_value))

    max_distance = []
    for movie_id in both_rated:
        u1rating = user1.ratings[movie_id]
        u2rating = user2.ratings[movie_id]
        sum_rating = abs(u1rating-u2rating)
        max_distance.append(sum_rating)
    return (((max(max_distance))*0.75)+(0.125*age_factor)+(0.125*gender_value))


def euclidean_distance(user1,user2,user1_age,user2_age,user1_gender,user2_gender):

    both_rated = set(user1.ratings.keys()) & set(user2.ratings.keys())
    total =0
    if user1_gender == user2_gender:
        gender_value =0
    else :
        gender_value =1
    age_gap = abs(user1_age - user2_age)
    if age_gap <10:
        age_factor = 0
    elif age_gap > 10 and age_gap<20:
        age_factor = 0.25
    elif age_gap>=20 and age_gap< 30:
        age_factor = 0.5
    elif age_gap>=30 and age_gap<40 :
        age_factor =0.75
    else:
        age_factor =1

    if len(both_rated) == 0:
        return ((0.125*age_factor)+(0.125*gender_value))

    for movie_id in both_rated:
        u1rating = user1.ratings[movie_id]
        u2rating = user2.ratings[movie_id]
        sum_rating = (u1rating-u2rating)**2
        total += sum_rating
    euclideandistance = math.sqrt(total)
    return ((euclideandistance*0.75)+(0.125*age_factor)+(0.125*gender_value))

def Manhattan_distance(user1,user2):
    common_ratings = set(user1.ratings.keys()) & set(user2.ratings.keys())
    total = 0
    if len(common_ratings) == 0:
        return 0

    for movie_id in common_ratings:
        user1rating = user1.ratings[movie_id]
        user2rating = user2.ratings[movie_id]
        sum = (user1rating-user2rating)
        total += sum
    return total
