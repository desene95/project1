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

class LogInForm(FlaskForm):
	username = StringField('username', validators=[InputRequired()])
	password = PasswordField('password', validators=[InputRequired()])
	remember = BooleanField('remember me')
	searchitem = StringField('searchitem')


class Credential(db.Model):
	userid = db.Column('userid', db.Integer, primary_key=True)
	FirstName = db.Column('FirstName', db.String(100))
	LastName = db.Column('LastName', db.String(100))
	username = db.Column('username', db.String(100), unique=True)
	password = db.Column('password', db.String(100))

	def __init__(self,FirstName, LastName, username, password): #SPecifies components of credential
		self.FirstName = FirstName
		self.LastName = LastName
		self.username = username
		self.password = password
db.create_all()

class Books2(db.Model):
    ISBN = db.Column('ISBN',db.String(300), primary_key=True)
    Title = db.Column('Title', db.String(300))
    Author = db.Column('Author', db.String(300))
    Year = db.Column('Year',db.Integer)

class Books3(db.Model):
    ISBN = db.Column('ISBN',db.String(300), primary_key=True)
    Title = db.Column('Title', db.String(300))
    Author = db.Column('Author', db.String(300))
    Year = db.Column('Year',db.Integer)
    Comment =  db.Column('Comment', db.String(1000))
    Ratings = db.Column('Ratings', db.Integer)


class Review1(db.Model):

    rat_id = db.Column('Rating ID',db.Integer, primary_key=True)
    rat_book = db.Column('Book', db.String(1000))
    rat_review = db.Column('Review', db.String(1000))

    def __init__(self, rat_book, rat_review):

        self.rat_book = rat_book
        self.rat_review = rat_review






@app.route('/')
def index():
	return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST']) #adds a user
def signup():
	if request.method == 'POST':
		result3 = request.form['FirstName']
		result4 = request.form['LastName']
		result = request.form['username']
		result2 = request.form['password']


		new_user = Credential(result3, result4, result, result2)
		db.session.add(new_user)
		db.session.commit()
		return "User added"
	return render_template('login.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LogInForm()
	if form.validate_on_submit():
		user = Credential.query.filter_by(username=form.username.data).first()
		if  user:
			if user.password == form.password.data:
				return redirect(url_for('dashboard'))
		return render_template("invalid.html", form=form)
	return render_template('Sign_in.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	#form = LogInForm()
	#if form.validate_on_submit():
		#return redirect(url_for('search'))
			#search1 = Books2.query.filter_by(searchitem=form.searchitem.data).first()
			#if search1:
				#if search1.Title == form.searchitem.data:


			#return '<h1> enter a legit value</h1>'
	allbooks = Books3.query.all()
	return render_template('dashboard.html', allbooks=allbooks)

@app.route("/search", methods = ['GET', 'POST'])
def search():
	if request.method == 'POST':
		form = request.form
		search_value = form['search_string']
		search = "%{}%".format(search_value)
		results = Books3.query.filter(Books3.Title.like(search)).all()
		return render_template('search.html', allbooks=results, legend="Search Results")



@app.route('/dashboard/<Title>/<Author>/<Year>/<Comment>', methods = ['GET', 'POST'])
def page(Title, Author, Year, Comment):


	return render_template('irobot.html', Title=Title, Author=Author, Year=Year, Comment=Comment)

@app.route('/api/<ISBN>', methods=['GET', 'POST'])
def api (ISBN):

	res = requests.get("https://www.goodreads.com/book/review_counts.json?key=qRCu1on2jgTdAJwQdGYw",
					   params={"isbns": ISBN})
	if res.status_code == 200:
		allISBN = Books3.query.filter(ISBN).first()
		data=res.json()

		return render_template("review.html", data=data, ISBN=ISBN, allISBN=allISBN)



@app.route('/review/<ISBN>/<Title>', methods=['GET','POST'])
def reviews(ISBN, Title):


	res = requests.get("https://www.goodreads.com/book/review_counts.json?key=qRCu1on2jgTdAJwQdGYw",
					   params={"isbns": ISBN})
	if res.status_code == 200:
		data = res.json()



		return render_template('review.html', ISBN=ISBN, data=data, Title=Title)

@app.route("/reviewtab", methods=['GET','POST'])
def revfunc():
	if request.method == 'POST':
		rev= request.form['rat_book']
		rev1 = request.form['rat_review']



		new_comment = Review1(rev, rev1)

		db.session.add(new_comment)
		db.session.commit()
		return "Review added"
	return render_template('review.html')




if __name__ == "__main__":
	app.run()


