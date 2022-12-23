from flask import Blueprint, request, jsonify, redirect, url_for
from streaming_location.helpers import token_required
from streaming_location.models import db, Title, movie_title_schema, movie_titles_schema
from streaming_location.forms import UserSearchForm
from datetime import datetime
import os
import requests

#crud

api = Blueprint('api', __name__, url_prefix = '/api')

#movie 
@api.route('/titles', methods = ['POST'])
@token_required
def parent_movies(token):
    title = request.form.get('original_title')
    database_id = request.form.get('id')
    key_art = request.form.get('ket_art')
    streaming_platform = request.form.get['streaming_platform']
    title = Title(title, database_id, key_art, streaming_platform, user_token=token)

    db.session.add(title)
    db.session.commit()
    
    return redirect(url_for('site.profile'))

#tv (future update)
# @api.route('/tvtitles', methods = ['POST'])
# @token_required
# def get_tv_title(token):
#     title = request.form.get('original_title')
#     database_id = request.form.get('id')
#     key_art = request.form.get('ket_art')

#     title = MovieTitle(title, database_id, key_art, user_token=token)

#     db.session.add(title)
#     db.session.commit()
    
#     return redirect(url_for('site.profile'))

#get one saved title
@api.route('/titles<id>', methods= ['GET'])
@token_required
def movie_title(id):
    title = Title.query.get(id)
    response = movie_title_schema.dump(title)

    return jsonify(response)


#get all saved titles
@api.route('/titles', methods = ['GET'])
@token_required
def movie_titles(token):
    title = Title.query.filter_by(user_token=token).all()
    response = movie_titles_schema.dump(title)

    return jsonify(response)

#update saved titles
@api.route('/titles<id>', methods = ['POST', 'PUT'])
@token_required
def update_movie_title(id):
    title = Title.query.get(id)
    title.title = request.json['title']
    title.database_id = request.json['id']
    title.streaming_platform = request.json['streaming_platform']
    title.key_art = request.json['key_art']
    response = movie_title_schema.dump(title)

    return jsonify(response)

#delete saved titles
@api.route('/titles/delete', methods = ['POST'])
@token_required
def delete_movie_title():
    database_id = request.form.get('id')
    title = Title.query.filter_by(database_id = database_id).first()
    db.session.delete(title)
    db.session.commit()

    return redirect(url_for('site.collection'))

# api calls

API_KEY = os.environ.get('API_KEY')
URL = 'https://api.themoviedb.org/3'

#searches
def movie_search(title):
    movie_title = requests.get(f'{URL}/search/movie/?api_key={API_KEY}&language=en-US&query={title}&page=1&include_adult=false').json()
    if movie_title['results']:
        movie_title_search = movie_search_results(movie_title['results'])

    return movie_title_search

#streaming finding for future update
def movie_streaming_search(movie_id):
    movie_stream = requests.get(f'{URL}/movie/{movie_id}/watch/providers')
    movie_stream_search = movie_stream_results(movie_stream['results'])

    return movie_stream_search

#tv future
# def tv_search():
#     tv_title = requests.get(f'')
#     if tv_title['tv_findings']:
#         tv_title_search = tv_search_results(tv_title['findings'])

    # return tv_title_search

# def tv_streaming_search():
#     tv_stream = requests.get(f'')
#     tv_stream_search = tv_stream_results

#search results

def movie_search_results(the_big_list):
    movie_title_results = []
    for movie_title in the_big_list:
        database_id = str(movie_title.get('id'))
        title = movie_title.get('original_title')
        key_art = movie_title.get('poster_path')

        if key_art:
            movie_title_object = Title(database_id=database_id,title=title, streaming_platform='streaming_platform', key_art=key_art, user_token='token')
            movie_title_results.append(movie_title_object)

    print(movie_title_results)

    return movie_title_results

#for future update
def movie_stream_results(movie_stream_list):
    movie_streaming_results = []
    for movie_streaming in movie_stream_list:
        streaming_platform = movie_streaming.get(['results']['US']['flatrate'])
        streaming_logo = movie_streaming.get(['results']['US']['logo_path'])
        
        if streaming_logo:
            movie_title_object = Title(streaming_platform, streaming_logo)
            movie_stream_results.append(movie_title_object)

        movie_streaming_results.append(movie_streaming)
    
    return movie_streaming_results

#tv_future
# def tv_search_results(tv_title_list):
#     tv_title_results = []
#     for tv_title_item in tv_title_list:
#         id = tv_title_item.get('')
#         title = tv_title_item.get('')
#         key_art = tv_title_item.get('')

#         if key_art:
#             tv_title_object = TvTitle(id, title, key_art)
#             tv_title_results.append(tv_title_object)

# tv streaming results future update
# def tv_stream_results(tv_stream_list):
#     tv_streaming_results = []
#     for 