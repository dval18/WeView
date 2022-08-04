from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from forms import PostForm, SearchForm, RegistrationForm, LoginForm, CommentForm
from flask_bcrypt import Bcrypt
from clearbitAPI import CompaniesList, clearbitInformation
import functools

import random
import requests
import os
import bcrypt

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '0336defeb890bb7bac96671c768bda2e'
#app.config['SECRET_KEY'] = '0cff8064643810cf406057022287b4c5'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  comments = db.relationship("Comment", backref="user", lazy=True)
  reviews = db.relationship("Review", backref="user", lazy=True)
  def __repr__(self):
    return f"User('{self.username}')"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    job_title = db.Column(db.String(50))
    response = db.Column(db.Text())
    company_id = db.Column(db.String(50), db.ForeignKey('company.id'),
        nullable=False)
    comments = db.relationship("Comment", backref="review", lazy=True)
    username = db.Column(db.String(20), db.ForeignKey('user.username'), 
        nullable=False)
    
    def __repr__(self):
        response = {'id':self.id, 'title':self.title, 'body':self.response, 'company':self.company_id}
        return str(response)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.Text())
    review_id = db.Column(db.String(50), db.ForeignKey('review.id'), 
        nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('user.username'), 
        nullable=False)
    
    def __repr__(self):
        response = {'id':self.id, 'response':self.response, 'review':self.review_id}
        return str(response)

class Company(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    reviews = db.relationship("Review", backref="company", lazy=True)

def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def is_logged_in(func):
    @functools.wraps(func)
    def secure_other(*args, **kwargs):
        if "username" in session:
            return redirect(url_for("reviews"))
        return func(*args, **kwargs)
    return secure_other

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page',
                         text='This is the home page')

@app.route("/post", methods=['GET','POST'])
@login_required
def post():
    form = PostForm()
    # List of all companies
    companies = CompaniesList()
    companies.insert(0, "")
    
    form.select.choices = companies

    if form.validate_on_submit():
        # company info is form.select.data
        # title is form.title.data
        # review data is form.text.data
        review = Review(title=form.title.data, username=session["username"], job_title=form.job_title.data, response=form.text.data, company_id=form.select.data)
        db.session.add(review)
        db.session.commit()
        flash('Review posted!', 'success')
        return redirect(url_for('reviews'))
    
    return render_template('post_review.html', user=session['username'], title='Post Form', form=form, choice_data=companies)

@app.route("/profile")
@login_required
def profile():
    user = User.query.filter_by(username=session['username']).first()
    return render_template('profile.html', user=user.username, reviews=user.reviews, comments=user.comments)

@app.route("/register", methods=['GET', 'POST'])
@is_logged_in
def register():
    form = RegistrationForm()
    existing_users_with_username = User.query.filter_by(username=form.username.data).all()
    if form.validate_on_submit() and len(existing_users_with_username) == 0: # checks if entries are valid
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=pw_hash)
        db.session.add(user)
        db.session.commit() 
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    elif len(existing_users_with_username) != 0:
        flash(f'Account already exists for {form.username.data}', 'failure')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
@is_logged_in
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            #print(user.password)
            if bcrypt.check_password_hash(user.password, form.password.data):
                print("hei")
                session['username'] = user.username
                return redirect(url_for('profile'))
        
    return render_template('login.html', title="Login", form=form)

@app.route("/logout")
@login_required
def logout():
    user = session["username"]
    session.clear()
    flash(f'{user} is logged out!', 'success')
    return redirect(url_for("home"))

@app.route("/read", methods=['GET','POST'])
@login_required
def read():
    source = request.args.get('id')
    if source is not None and source.isnumeric():
        review = Review.query.filter_by(id=source).first()
        comment_form = CommentForm()

        if comment_form.validate_on_submit():
            comment = Comment(response=comment_form.text.data, review_id=review.id, username=session["username"])
            db.session.add(comment)
            db.session.commit()
            comments = Comment.query.filter_by(review_id=review.id).all()
            flash(f'Review posted!', 'success')

            return render_template('read_review.html', user=session['username'], review=review, form=comment_form, num_comments=len(comments), comments=comments)
        else:    
            comments = Comment.query.filter_by(review_id=review.id).all()
            return render_template('read_review.html', user=session['username'], review=review, form=comment_form, num_comments=len(comments), comments=comments)
    else:
        return render_template('error_after_login.html', error_message='Invalid Input', error_text='Invalid or no ID entered')


@app.route("/reviews", methods=['GET','POST'])
@login_required
def reviews():
    form = SearchForm()

    #list of all companies
    companies = CompaniesList()
    companies.insert(0, "")

    form.select.choices = companies
    all_revs = Review.query.all()

    if form.validate_on_submit():
        reviews = Review.query.filter_by(company_id=form.select.data).all()
        company = clearbitInformation(form.select.data)
        img_info = company["logo"]
        desc = company["description"]
        linkedin = company["linkedin"]
        domain = company["domain"]
        return render_template('reviews.html', user=session['username'], form=form, domain=domain, reviews=reviews, title=f'{form.select.data} Reviews', img_url=img_info, description=desc, linkedin=linkedin)

    return render_template('reviews.html', user=session['username'], form=form, reviews=all_revs, title="All Reviews", img_url="../static/styles/images/logo_dark.jpeg")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
