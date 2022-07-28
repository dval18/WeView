from flask import Flask, render_template, url_for, flash, redirect
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import random
import requests
import os

app = Flask(__name__)

proxied = FlaskBehindProxy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page',
                         text='This is the home page')






if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
