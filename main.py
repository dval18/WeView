from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy

from forms import PostForm, SearchForm, RegistrationForm, LoginForm

import random
import requests
import os

app = Flask(__name__)

proxied = FlaskBehindProxy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '0336defeb890bb7bac96671c768bda2e'
app.config['SECRET_KEY'] = '0cff8064643810cf406057022287b4c5'


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page',
                         text='This is the home page')

@app.route("/post", methods=['GET','POST'])
def post():
    form = PostForm()

    # List of all companies
    companies = ["Placeholder text", "ab", "bc", "cd", "de", "ef", "fg", "gh", "hi", "ij", "jk", "kl", "lm", "mn", "no", 
                            "op", "pq", "qr", "rs", "st", "tu", "uv", "vw", "wx", "xy", "yz"]

    #TODO: Change this to the list of inputs from the api
    form.select.choices = companies

    if form.validate_on_submit():
        # company info is form.select.data
        # review data is form.text.data
        return redirect(url_for('reviews'))

    return render_template('post_review.html', title='Post Form', form=form, choice_data=companies)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

<<<<<<< HEAD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}')"
=======
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', title="Login", form=form)
>>>>>>> 95f5cda72258cb9b10e9e98b39f0836027e9d60b


@app.route("/read")
def read():
    source = request.args.get('id')
    if source is not None:
        try:
            # we should assign each review an id in order to grab the necessary data
            source = int(source)  # make sure that it's an int (for id purposes)

            # ideally we would get a review formatted like this? with any other data we think should be added
            review = {'title':'placeholder title info', 'body':'placeholder body info'}
            return render_template('read_review.html', review=review)
        except ValueError:
            return render_template('error_after_login.html', error_message='Invalid Input', error_text='Invalid or no ID entered')
    else:
        return render_template('error_after_login.html', error_message='Invalid Input', error_text='Invalid or no ID entered')

@app.route("/reviews", methods=['GET','POST'])
def reviews():
    form = SearchForm()

    #list of all companies
    companies = ["Placeholder text", "ab", "bc", "cd", "de", "ef", "fg", "gh", "hi", "ij", "jk", "kl", "lm", "mn", "no", 
                            "op", "pq", "qr", "rs", "st", "tu", "uv", "vw", "wx", "xy", "yz"]

    form.select.choices = companies

    all_revs = []

    # mock data of all reviews for this page
    # will want a list of dictionaries {id:id, title:title}
    # at least for the actual review part
    for i in range(len(companies)):
        whole = {'id':i, 'title':'Dummy Title', 'company':companies[i]}
        all_revs.append(whole)

    if form.validate_on_submit():
        #reviews is where I'll send the reviews that correspond to the chosen company
        to_send = []

        for i in range(len(all_revs)):
            if form.select.data == all_revs[i]['company']:
                to_send.append(all_revs[i])

        return render_template('reviews.html', form=form, reviews=to_send, title=f'{form.select.data} Reviews')

    return render_template('reviews.html', form=form, reviews=all_revs, title="All Reviews")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
