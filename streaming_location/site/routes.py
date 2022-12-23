from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from streaming_location.api.routes import URL, API_KEY, movie_search, movie_streaming_search
from streaming_location.forms import UserSearchForm
from streaming_location.helpers import token_required

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    # favorite_movies = favorite_movies()
    # titles = MovieTitle.query.filter_by(user_token = current_user.token).all()
    return render_template('profile.html')


@site.route('/collection', methods= ['GET', 'POST'])
@login_required
def collection():
    
    collection_form = UserSearchForm()
    print(collection_form.errors)
    print("hello you've found me")

    try:
        if request.method == 'POST' and collection_form.validate_on_submit():
            print('hello again')
            search = collection_form.title.data
            results = movie_search(search)
            return render_template('movie_results.html', results = results)
        else:
            print('else')
    except:
        raise Exception('Invalid Data: Please check the name of your movie and try again')
    
    return render_template('collection.html', collection_form = collection_form)
