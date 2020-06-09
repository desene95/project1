from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, length
from flask_bootstrap import Bootstrap
import csv
import psycopg2
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisismysecretkey'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ose1234@localhost/Users'
app.debug = True
db = SQLAlchemy(app)

class Books3(db.Model):
    ISBN = db.Column('ISBN',db.String(300), primary_key=True)
    Title = db.Column('Title', db.String(300))
    Author = db.Column('Author', db.String(300))
    Year = db.Column('Year',db.Integer)
    Comment =  db.Column('Comment', db.String(1000))
    Ratings = db.Column('Ratings', db.Integer)

    def __init__(self, ISBN, Title, Author, Year, Comment, Ratings):
        self.ISBN = ISBN
        self.Title = Title
        self.Author = Author
        self.Year = Year
        self.Comment = Comment
        self.Ratings = Ratings

db.create_all()






if __name__ == "__main__":
    with app.app_context():
        main()
