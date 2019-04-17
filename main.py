from database import DataBase
from flask import Flask, render_template, url_for

filename = 'database1'
db = DataBase(filename)

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', title="Movies DataBase")

@app.route('/list_of_movies')
def ListOfMovies():
	array = db.ListOfMovies()
	#return render_template('ListOfMovies.html', title="List of movies", array=array)
	return "smth"


@app.route('/list_of_people')
def ListOfPeople():
	array = db.ListOfPeople()
	return render_template('ListOfPeople.html', title="List of people", array=array)

@app.route('/movie/movie_id=<int:movie_id>')
def movie(movie_id):
	return "Will be showing data for specified movie"

@app.route('/person/person_id=<int:person_id>')
def person(person_id):
	return "Will be showing data for specified person!"
	# return render_template('person.html', name=name)