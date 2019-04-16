import sqlite3
"""
Some examples of working with sqlite3. More is via this link: https://docs.python.org/3.6/library/sqlite3.html
	connection = sqlite3.connect('filename')
	c = connection.cursor()
	c.execute("SOME SQL QUERY")
	connection.commit()
	connection.close()
"""

# FIXME: fetchone() returns a tuple (object, )!!!
# year is INTEGER - is it good?

class DataBase:
	def __init__(self, filename):
		self.db = sqlite3.connect(filename)
		self.cursor = self.db.cursor()
		self.movies = Movies(self.cursor)
		self.persons = Persons(self.cursor)
		self.countries = Countries(self.cursor)
		self.jobs = Jobs(self.cursor)
		self.moviecountry = MovieCountry(self.cursor)
		self.moviepersonjob = MoviePersonJob(self.cursor)

	def commit(self):
		self.db.commit()

	def rollback(self):
		self.db.rollback()

	def close(self):
		self.db.close()

	def ListOfMovies(self):
		# returns list of tuples (movie_id, movie_title) or empty list
		return self.cursor.execute("SELECT id, title FROM Movies;").fetchall()

	def ListOfPeople(self):
		# returns list of tuples (person_id, name) or empty list
		return self.cursor.execute("SELECT id, name FROM Persons;").fetchall()

	def ShowMovie(self, movie_id):
		# TODO: CHECK IF EXISTS
		title, year = self.cursor.execute("""SELECT title, production_year FROM Movies 
			WHERE id = ?;""", [movie_id]).fetchone()
		participants_ids = self.moviepersonjob.ShowPeopleInvolvedIDs(movie_id)
		participants = [(self.persons.ShowNameByID(person_id), self.jobs.ShowJobByID(job_id)) \
			for person_id, job_id in participants_ids]
		countries = self.moviecountry.ShowCountriesInvolved(movie_id)
		return title, year, participants, countries

	def ShowPerson(self, person_id):
		# returns tuple (name, year, filmography); filmography is a list of tuples [Title, Job]
		# TODO: CHECK IF EXISTS
		name, birth_year = self.persons.ShowPersonalInfoByID(person_id)
		filmography_ids = self.moviepersonjob.ShowFilmographyWithIDs()
		filmography = [(self.movies.ShowTitleByID(movie_id), self.jobs.ShowJobByID(job_id)) \
			for movie_id, job_id in filmography_ids]
		return name, birth_year, filmography


class Movies:
	def __init__(self, cursor):
		self.cursor = cursor
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS Movies (
								id INTEGER PRIMARY KEY AUTOINCREMENT, 
								title TEXT NOT NULL,
								production_year INTEGER NOT NULL);""")

	def ShowTitleByID(self, movie_id):
		# TODO: CHECK IF EXISTS
		return self.cursor.execute("SELECT title FROM Movies WHERE id = ?;", [movie_id]).fetchone()


def Persons:
	def __init__(self, cursor):
		self.cursor = cursor
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS Persons (
								id INTEGER PRIMARY KEY AUTOINCREMENT, 
								name TEXT NOT NULL,
								birth_year INTEGER NOT NULL);""")

	def ShowPersonalInfoByID(self, person_id):
		return self.cursor.execute("SELECT name, birth_year FROM Persons WHERE id = ?", 
			[person_id]).fetchone()

	def ShowNameByID(self, person_id):
		return self.cursor.execute("SELECT name FROM Persons WHERE id = ?", [person_id]).fetchone()


class Countries:
	def __init__(self, cursor):
		self.cursor = cursor
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS Countries (
								id INTEGER PRIMARY KEY AUTOINCREMENT, 
								name TEXT NOT NULL);""")

class Jobs:
	def __init__(self, cursor):
		self.cursor = cursor
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS Jobs (
								id INTEGER PRIMARY KEY AUTOINCREMENT, 
								job TEXT NOT NULL);""")

	def ShowJobByID(self, job_id):
		return self.cursor.execute("SELECT title FROM Jobs WHERE id = ?;", [job_id]).fetchone()


class MovieCountry:
	def __init__(self, cursor):
		self.cursor = cursor
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS MovieCountry (
								id_movie INTEGER, 
								id_country INTEGER);""")

	# FIXME!!! Function also looks for data from table Countries - is it OK?
	def ShowCountriesInvolved(self, movie_id):
		return self.cursor.execute("""SELECT name FROM Countries WHERE id = (
			SELECT id_country FROM MovieCountry WHERE id_movie = ?);""", 
			[movie_id]).fetchall()


class MoviePersonJob:
	def __init__(self, cursor):
		self.cursor = cursor
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS MoviePersonJob (
								id_movie INTEGER, 
								id_person INTEGER, 
								id_job INTEGER);""")

	def __ShowFilmographyWithIDs(person_id):
		return self.cursor.execute("""SELECT id_movie, id_job FROM MoviePersonJob 
			WHERE id_person = ?;""", [person_id]).fetchall()

	def ShowPeopleInvolvedIDs(movie_id):
		return self.cursor.execute("""SELECT id_person, id_job FROM MoviePersonJob 
			WHERE id_movie = ?;""", [movie_id]).fetchall()
