from database import DataBase

filename = 'database2.db'

db = DataBase(filename)

r1 = db.AddPersonCountry("Rupert Grint", "UK")
r2 = db.AddPersonCountry("Michael Caine", "USA")

print(r1, r2)

if r1 and r2:
	db.commit()

db.close()