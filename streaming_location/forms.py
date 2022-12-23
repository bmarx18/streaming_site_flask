from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
# from streaming_location.models import db

class UserLoginForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()

# create title form
class UserSearchForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    submit_button = SubmitField()

#create favorite form
# class UserFavorites(FlaskForm):
#     tv_title = StringField('TvTitle')
#     database_id = StringField('ID')