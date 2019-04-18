from database import DataBase

filename = 'database2.db'

db = DataBase(filename)
"""
print("Movies before adding any:")
print(db.ListOfMovies())

print("People before adding any:")
print(db.ListOfPeople())

results = []
r1 = db.AddEntry("Harry Potter and the Philosopher's Stone", 2001, [
	('Chris Columbus', 1958, 'Director'), 
	('Daniel Radcliffe', 1989,'Actor'), 
	('Rupert Grint', 1988, 'Actor'), 
	('Emma Watson', 1990, 'Actor')],
		 ["UK", "USA"])

r2 = db.AddEntry("Harry Potter and the Prisoner of Azkaban", 2001, [
	('Alfonso Cuaron', 1961, 'Director'), 
	('Chris Columbus', 1958, 'Producer'), 
	('Daniel Radcliffe', 1989,'Actor'), 
	('Rupert Grint', 1988, 'Actor'), 
	('Emma Watson', 1990, 'Actor')],
		 ["UK", "USA"])

r3 = db.AddEntry("Interstellar", 2014, [
	('Christopher Nolan', 1970, 'Writer'), 
	('Christopher Nolan', 1970, 'Producer'), 
	('Anne Hathaway', 1982,'Actor'), 
	('Michael Caine', 1933, 'Actor')], 
		["UK", "USA"])

print("Results:", r1, r2, r3)
"""
print("Movies:")
print(db.ListOfMovies())

print("People:")
print(db.ListOfPeople())

print("Some movie:")
print(db.ShowMovie(2))

print("Some person:")
print(db.ShowPerson(1))

db.close()