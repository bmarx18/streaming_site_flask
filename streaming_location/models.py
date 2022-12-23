from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import uuid
from werkzeug.security import generate_password_hash
import secrets
from datetime import datetime
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    titles = db.relationship('Title', backref='owner', lazy = True)
    # tv_titles = db.relationship('TvTitle', backref='owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify


    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database!'

class MovieTitleObject:
    def __init__(self, id, title, streaming_platform, key_art):
        self.id = id
        self.title = title
        self.streaming_platform = f'{streaming_platform}'
        self.key_art = f'https://image.tmdb.org/t/p/w500/{key_art}'

class Title(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(150))
    database_id = db.Column(db.String())
    streaming_platform = db.Column(db.String())
    key_art = db.Column(db.String())
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, title, database_id, streaming_platform, key_art, user_token, id = ''):
        self.id = self.set_id()
        self.title = title
        self.database_id = database_id
        self.streaming_platform = streaming_platform
        self.key_art = key_art
        self.user_token = user_token

    def __repr__(self):
        return f'The following movie title has been added: {self.title}'

    def set_id(self):
        return secrets.token_urlsafe()


#tv class future update
#class TvTitle(db.Model):

#creating movie api schema

class MovieTitleSchema(ma.Schema):
    class Meta:
        fields = ['id', 'title', 'database_id', 'streaming_platform', 'key_art']

movie_title_schema = MovieTitleSchema()
movie_titles_schema = MovieTitleSchema(many = True)

#creating tv api schema 

#class TVTitleSchema(ma.Schema):
#     class Meta:
#         fields = ['id', 'title', 'database_id', 'streaming_platforms', 'key_art']

# tv_title_schema = TvTitleSchema()
# tv_titles_schema = TvTitleSchema(many = True)