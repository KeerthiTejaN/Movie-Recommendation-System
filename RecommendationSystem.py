from __future__ import division
import DistanceFuns as base
import csv

def user_to_user_distance(training_data,user_details,movie_details):
    Data_list = base.data_tuple(training_data)
    Users_diction = base.users_data(Data_list)
    Movies_diction = base.movie_data(Users_diction)
    user_keys = Users_diction.keys()
    Dist_diction ={}
    for i in range(0,len(user_keys)):
        distance = []
        user1_id = user_keys[i]
        user1_details = Users_diction[user1_id]
        user1_age = int(user_details[str(user1_id)]['age'])
        user1_gender = user_details[str(user1_id)]['gender']

        for j in range(i,len(user_keys)):
            user2_id = user_keys[j]
            user2_values = Users_diction[user2_id]
            user2_age = int(user_details[str(user2_id)]['age'])
            user2_gender = user_details[str(user2_id)]['gender']

            euclidean_distance = base.lmax_distance(user1_details, user2_values,user1_age,user2_age,user1_gender,user2_gender)
            distance.append((euclidean_distance,user2_id))
        Dist_diction[user1_id] = sorted(distance)
    return Dist_diction,Users_diction,Movies_diction

def predict_rating(user_diction, distances, uid, movie_id, movie):
    k = 20
    count = 0
    predrat = 0
    for umrs in distances:
        u_key = umrs[1]
        u_value = user_diction[u_key]
        if u_value.rated_movie(movie_id):
            predrat += u_value.average + u_value.ratings[movie_id]
            count +=1
        if count == k:
            break
    return int(round(predrat/k))

def mainfunctioncall(training_filename, test_filename):

    MAD =0
    no_of_users =0
    movie_details ={}
    f = open('/Users/KeerthiTejaNuthi/Documents/ml-100k/u.item')
    lines = f.readlines()
    for line in lines:
        split_line = line.split('|')
        movie_details[split_line[0]] = {
            'title': split_line[1],
            'release date': split_line[2],
            'video release date': split_line[3],
            'IMDB URL': split_line[4],
            'Genres': genre(split_line)
        }
    f.close()
    user_details = {}
    f = open('/Users/KeerthiTejaNuthi/Documents/ml-100k/u.user')
    ulinees = f.readlines()
    for ulinee in ulinees:
        cut = ulinee.split('|')
        user_details[cut[0]] = {
            'age': cut[1],
            'gender': cut[2],
            'occupation': cut[3]
        }
    f.close()
    distance_diction, users_diction, movie_diction = user_to_user_distance(training_filename,user_details,movie_details)
    with open(test_filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        count =0
        for linee in reader:
            uID = int(linee[0])
            mID = int(linee[1])
            act_rating = int(linee[2])
            if uID in distance_diction and mID in movie_diction:
                predicted_rating = predict_rating(users_diction,distance_diction[uID],uID,mID,movie_diction)
                MAD += abs(predicted_rating-act_rating)
                no_of_users += 1
                if act_rating == predicted_rating:
                    count +=1
        accuracy = count/no_of_users
        final_MAD = MAD/no_of_users
        print "Mean Absolute Difference MAD is {0}, accuracy is {1} ",final_MAD,accuracy


def genre(chosen_line):
	movie_genre = chosen_line[5:]
	Genre_diction = { 	0: "unknown",
					1: "Action",
					2: "Adventure",
					3: "Animation",
					4: "Children's",
					5: "Comedy",
					6: "Crime",
					7: "Documentary",
					8: "Drama",
					9: "Fantasy",
					10: "Film-Noir",
					11: "Horror",
					12: "Musical",
					13: "Mystery",
					14: "Romance",
					15: "Sci-Fi",
					16: "Thriller",
					17: "War",
					18: "Western" }
	genres = []
	for index, num in enumerate(movie_genre):
		if num == '1':
			genres.append(Genre_diction[index])
	return genres



mainfunctioncall('/Users/KeerthiTejaNuthi/Documents/ml-100k/u1.base','/Users/KeerthiTejaNuthi/Documents/ml-100k/u1.test')
