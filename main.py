from database import DataBase
from flask import Flask, render_template, url_for

filename = 'database2.db'
db = DataBase(filename, CheckingSameThread=False)

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', title="Movies DataBase")

@app.route('/list_of_movies')
def ListOfMovies():
	return render_template('list_of_movies.html', title="List of movies", array=db.ListOfMovies())

@app.route('/list_of_people')
def ListOfPeople():
	return render_template('list_of_people.html', title="List of people", array=db.ListOfPeople())

@app.route('/movie/movie_id=<int:movie_id>')
def movie(movie_id):
	title, year, participants, countries = db.ShowMovie(movie_id)
	return render_template('movie.html', MovieTitle=title, production_year=year, 
		countries=countries, participants=participants)

@app.route('/person/person_id=<int:person_id>')
def person(person_id):
	name, birth_year, filmography = db.ShowPerson(person_id)
	return render_template('person.html', name=name, birth_year=birth_year, filmography=filmography)
