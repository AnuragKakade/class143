from flask import Flask,jsonify,request
import csv
from demographic import output
from content import get_recommendations

app=Flask(__name__)

all_movies=[]
liked_movies=[]
disliked_movies=[]
not_watched_movies=[]

with open('final.csv',encoding='utf8') as f:
    reader=csv.reader(f)
    data=list(reader)
    all_movies=data[1:]

@app.route('/get-movie')
def get_movie():
    movie_data = { "title": all_movies[0][19],
          "poster_link": all_movies[0][27], 
          "release_date": all_movies[0][13] or "N/A", 
          "duration": all_movies[0][15], 
          "rating": all_movies[0][20], 
          "overview": all_movies[0][9] }
    return jsonify({
        'data':movie_data,
        'status':'success'
    })

@app.route('/liked-movie',methods=['POST'])
def liked_movie():
    movie=all_movies[0]
    all_movies.pop(0)
    liked_movies.append(movie)
    return jsonify({
        'status':'success'
    })

@app.route('/disliked-movie',methods=['POST'])
def disliked_movie():
    movie=all_movies[0]
    all_movies.pop(0)
    disliked_movies.append(movie)
    return jsonify({
        'status':'success'
    })

@app.route('/notwatched-movie',methods=['POST'])
def not_watched_movie():
    movie=all_movies[0]
    all_movies.pop(0)
    not_watched_movies.append(movie)
    return jsonify({
        'status':'success'
    })

@app.route('/popular-movies')
def popular_movies():
    global output
    movie_data=[]
    for movie in output:
        d={"title": movie[0],
          "poster_link": movie[1], 
          "release_date": movie[2] or "N/A", 
          "duration": movie[3], 
          "rating": movie[4],
          }
        movie_data.append(d)
    return jsonify({
        'data':movie_data,
        'status':'success'
    })
@app.route('/recommended-movies')
def recommended_movies():
    all_recommended=[]
    for liked_movie in liked_movies:
        result=get_recommendations(liked_movie)
        for data in result:
            all_recommended.append(data)
    all_recommended.sort()
    movie_data=[]
    for movie in all_recommended:
        d={"title": movie[0],
          "poster_link": movie[1], 
          "release_date": movie[2] or "N/A", 
          "duration": movie[3], 
          "rating": movie[4],
          }
        movie_data.append(d)
    return jsonify({
        'data':movie_data,
        'status':'success'
    })
app.run(debug=True)