from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=20)])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class PostForm(FlaskForm):
    company = StringField('Company')
    select = SelectField('Company', choices=[], validators=[DataRequired()])
    job_title = StringField('Job Title', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Review Text',
                           validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    text = TextAreaField('Comment Here!',
                           validators=[DataRequired()])
    submit = SubmitField('Post Comment')

class SearchForm(FlaskForm):
    company = StringField('Company')
    select = SelectField('Company', choices=[], validators=[DataRequired()])
    submit = SubmitField('Search')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
