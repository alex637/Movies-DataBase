import sqlite3
"""
Some examples of working with sqlite3. More is via this link: https://docs.python.org/3.6/library/sqlite3.html
	connection = sqlite3.connect('filename')
	c = connection.cursor()
	c.execute("SOME SQL QUERY")
	connection.commit()
	connection.close()
"""


class DataBase:
	def __init__(self, filename, CheckingSameThread=True):
		self.db = sqlite3.connect(filename, check_same_thread=CheckingSameThread)
		self.cursor = self.db.cursor()
		self.cursor.execute("PRAGMA foreign_keys=on;")
		self.movies = Movies(self.cursor)
		self.persons = Persons(self.cursor)
		self.countries = Countries(self.cursor)
		self.jobs = Jobs(self.cursor)
		self.moviecountry = MovieCountry(self.cursor)
		self.moviepersonjob = MoviePersonJob(self.cursor)
		self.personcountry = PersonCountry(self.cursor)

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
		# returns tuple (name, year, countries, filmography); filmography is a list of tuples [Title, Job]
		# TODO: CHECK IF EXISTS
		name, birth_year = self.persons.ShowPersonalInfoByID(person_id)
		filmography_ids = self.moviepersonjob._ShowFilmographyWithIDs(person_id)
		filmography = [(self.movies.ShowTitleByID(movie_id), self.jobs.ShowJobByID(job_id)) \
			for movie_id, job_id in filmography_ids]
		countries = self.personcountry.ShowCountries(person_id)
		return name, birth_year, countries, filmography

	def AddEntry(self, title, production_year, involvements, countries):
		"""
		Should be called with movie_title, production_year, [(NameOfPerson, BirthYear, Job)] - not empty!, [country,...] - not empty!
		returns True or False
		calls commit() if ok
		"""
		# TODO: check correctness of data provided
		production_year = str(production_year) # not sure if this is necessary
		if len(involvements) == 0 or len(countries) == 0:
			return False
		if self.cursor.execute("""SELECT COUNT(*) FROM Movies WHERE title = ? AND 
			production_year = ?;""", [title, production_year]).fetchone()[0] > 0:
			return False	# movie is already in the DB
		# functions below add(smth) only if it's not currently in the database
		movie_id = self.movies.AddMovie(title, production_year)
		for country in countries:
			country_id = self.countries.AddCountry(country)
			self.moviecountry.AddMovieCountry(movie_id, country_id)		
		for name, birth_year, job in involvements:
			person_id = self.persons.AddPerson(name, str(birth_year))
			job_id = self.jobs.AddJob(job)
			self.moviepersonjob.AddMoviePersonJob(movie_id, person_id, job_id)
		self.commit()
		return True

	def AddPersonCountry(self, person_name, country_name):
		person_id =  self.persons.ShowIDByName(person_name)
		country_id = self.countries.ShowIDByName(country_name)
		# DEBUG!!!
		print('person:', person_id, person_name)
		print('country:', country_id, country_name)
		if country_id is not None and person_id is not None:
			self.cursor.execute("INSERT INTO PersonCountry (id_person, id_country) VALUES (?, ?);",
				[person_id[0], country_id[0]])
			return True
		else:
			return False


class Movies:
	def __init__(self, cursor):
		self.cursor = cursor
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS Movies (
								id INTEGER PRIMARY KEY AUTOINCREMENT, 
								title TEXT NOT NULL,
								production_year INTEGER NOT NULL);""")

	def ShowTitleByID(self, movie_id):
		# TODO: CHECK IF EXISTS
		return self.cursor.execute("SELECT title FROM Movies WHERE id = ?;", [movie_id]).fetchone()[0]

	def AddMovie(self, movie_title, production_year):
		movie_id = self.cursor.execute("""SELECT id FROM Movies WHERE title = ? 
			AND production_year = ?;""", [movie_title, production_year]).fetchone()
		if movie_id is not None:
			movie_id = movie_id[0]
		else:
			self.cursor.execute("""INSERT INTO Movies (title, production_year) 
				VALUES (?, ?);""", [movie_title, production_year])
			movie_id = self.cursor.execute("""SELECT id FROM Movies WHERE title = ? 
				AND production_year = ?;""", [movie_title, production_year]).fetchone()[0]
		return movie_id


class Persons:
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
		return self.cursor.execute("SELECT name FROM Persons WHERE id = ?", [person_id]).fetchone()[0]

	def ShowIDByName(self, person_name):
		return self.cursor.execute("SELECT id FROM Persons WHERE name = ?", [person_name]).fetchone()

	def AddPerson(self, name, birth_year):
		person_id = self.cursor.execute("""SELECT id FROM Persons WHERE name = ? 
			AND birth_year = ?;""", [name, birth_year]).fetchone()
		if person_id is not None:
			person_id = person_id[0]
		else:
			self.cursor.execute("INSERT INTO Persons (name, birth_year) VALUES (?, ?);", 
				[name, birth_year])
			person_id = self.cursor.execute("""SELECT id FROM Persons WHERE name = ? 
				AND birth_year = ?;""", [name, birth_year]).fetchone()[0]
		return person_id


class Countries:
	def __init__(self, cursor):
		self.cursor = cursor
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS Countries (
								id INTEGER PRIMARY KEY AUTOINCREMENT, 
								name TEXT NOT NULL);""")

	def AddCountry(self, country):
		country_id = self.cursor.execute("SELECT id FROM Countries WHERE name = ?;",
			[country]).fetchone()
		if country_id is not None:
			country_id = country_id[0]
		else:
			self.cursor.execute("INSERT INTO Countries (name) VALUES (?);", [country])
			country_id = self.cursor.execute("SELECT id FROM Countries WHERE name = ?;",
				[country]).fetchone()[0]
		return country_id

	def ShowIDByName(self, country_name):
		return self.cursor.execute("SELECT id FROM Countries WHERE name = ?;", [country_name]).fetchone()


class Jobs:
	def __init__(self, cursor):
		self.cursor = cursor
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS Jobs (
								id INTEGER PRIMARY KEY AUTOINCREMENT, 
								job TEXT NOT NULL);""")

	def ShowJobByID(self, job_id):
		return self.cursor.execute("SELECT job FROM Jobs WHERE id = ?;", [job_id]).fetchone()[0]

	def AddJob(self, job):
		job_id = self.cursor.execute("SELECT id FROM Jobs WHERE job = ?;", [job]).fetchone()
		if job_id is not None:
			job_id = job_id[0]
		else:
			self.cursor.execute("INSERT INTO Jobs (job) VALUES (?);", [job])
			job_id = self.cursor.execute("SELECT id FROM Jobs WHERE job = ?;", [job]).fetchone()[0]
		return job_id


class MovieCountry:
	def __init__(self, cursor):
		self.cursor = cursor
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS MovieCountry (
								id_movie INTEGER, 
								id_country INTEGER,
								FOREIGN KEY (id_movie) REFERENCES Movies(id), 
								FOREIGN KEY (id_country) REFERENCES Countries(id));""")

	# FIXME!!! Function also looks for data from table Countries - is it OK?
	def ShowCountriesInvolved(self, movie_id):
		country_ids = self.cursor.execute("""SELECT id_country FROM MovieCountry WHERE
			id_movie = ?;""", [movie_id]).fetchall()
		results = []
		for country_id in country_ids:
			results.append(self.cursor.execute("""SELECT name FROM Countries WHERE 
				id = ?;""", [country_id[0]]).fetchone()[0])
		return results

	def AddMovieCountry(self, movie_id, country_id):
		self.cursor.execute("""INSERT INTO MovieCountry (id_movie, id_country) 
			VALUES (?, ?);""", [movie_id, country_id])


class MoviePersonJob:
	def __init__(self, cursor):
		self.cursor = cursor
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS MoviePersonJob (
								id_movie INTEGER, 
								id_person INTEGER, 
								id_job INTEGER, 
								FOREIGN KEY (id_movie) REFERENCES Movies(id), 
								FOREIGN KEY (id_person) REFERENCES Persons(id), 
								FOREIGN KEY (id_job) REFERENCES Jobs(id));""")

	def _ShowFilmographyWithIDs(self, person_id):
		return self.cursor.execute("""SELECT id_movie, id_job FROM MoviePersonJob 
			WHERE id_person = ?;""", [person_id]).fetchall()

	def ShowPeopleInvolvedIDs(self, movie_id):
		return self.cursor.execute("""SELECT id_person, id_job FROM MoviePersonJob 
			WHERE id_movie = ?;""", [movie_id]).fetchall()

	def AddMoviePersonJob(self, movie_id, person_id, job_id):
		self.cursor.execute("""INSERT INTO MoviePersonJob (id_movie, id_person,
			id_job) VALUES (?, ?, ?);""", [movie_id, person_id, job_id])

class PersonCountry:
	def __init__(self, cursor):
		self.cursor = cursor
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS PersonCountry (
								id_person INTEGER, 
								id_country INTEGER, 
								FOREIGN KEY (id_person)  REFERENCES Persons(id), 
								FOREIGN KEY (id_country) REFERENCES Countries(id) );""")

	def ShowCountries(self, person_id):
		country_ids = self.cursor.execute("""SELECT id_country FROM PersonCountry WHERE
			id_person = ?;""", [person_id]).fetchall()
		results = []
		for country_id in country_ids:
			results.append(self.cursor.execute("""SELECT name FROM Countries WHERE 
				id = ?;""", [country_id[0]]).fetchone()[0])
		return results

"""
	def AddPersonCountry(self, person_name, country_name):
		person_id =  self.persons.ShowIDByName(person_name)
		country_id = self.ShowIDByName(person_name)
		if country_id is not None and person_id is not None:
			self.cursor.execute("INSERT INTO PersonCountry (id_person, id_country) VALUES (?, ?);",
				[person_name[0], country_name[0]])
			return True
		else:
			return False
"""