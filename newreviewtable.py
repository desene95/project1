from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, length
from flask_bootstrap import Bootstrap
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisismysecretkey'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ose1234@localhost/Users'
app.debug = True
db = SQLAlchemy(app)

class Review1(db.Model):

    rat_id = db.Column('Rating ID',db.Integer, primary_key=True)
    rat_book = db.Column('Book', db.String(1000))
    rat_review = db.Column('Review', db.String(1000))

    def __init__(self,rat_book, rat_review):

        self.rat_book = rat_book
        self.rat_review = rat_review

db.create_all()

if __name__ == "__main__":
	app.run()
