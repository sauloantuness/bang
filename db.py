import sqlite3

DATABASE_FILE = "database.db"

class User():
	def __init__(self, uriId, name, userId=None):
		self.uriId = uriId
		self.name = name
		self.userId = userId

class Problem():
	def __init__(self, problemId, name, category, level, solved):
		self.problemId = problemId
		self.name = name
		self.category = category
		self.level = level
		self.solved = solved

class Solved():
	def __init__(self, userId, problemId, solvedId=None):
		self.userId = userId
		self.problemId = problemId

class DB():
	def __init__(self):
		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()
		c.execute("""CREATE TABLE IF NOT EXISTS users
					 (userId integer primary key autoincrement,
					  uriId text not null unique,
					  name text not null) """)

		c.execute("""CREATE TABLE IF NOT EXISTS problems
					 (problemId integer primary key not null,
					  name text not null,
					  category text not null,
					  level integer not null,
					  solved integer not null) """)

		c.execute("""CREATE TABLE IF NOT EXISTS solved
					 (solvedId integer primary key autoincrement,
					  userId integer,
					  problemId integer,
					  foreign key(userId) REFERENCES users(userId),
					  foreign key(problemId) REFERENCES problems(problemId)) """)

		conn.commit()
		conn.close()

		print 'Tables created with success.'

	def insertUser(self, user):
		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()
		c.execute("""INSERT INTO users (uriId,name) VALUES (?,?)""", (user.uriId, user.name) )
		user.userId = c.lastrowid
		conn.commit()
		conn.close()
		return user

	def deleteUser(self, user):
		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()
		c.execute("""DELETE FROM users where userId=?""", (user.userId,))
		conn.commit()
		conn.close()
		return user

	def getUsers(self):
		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()
		c.execute("""SELECT uriId, name, userId FROM users""")

		users = []
		for row in c.fetchall():
			user = User(uriId=row[0], name=row[1], userId=row[2])
			users.append(user)

		conn.close()

		return users

	def insertProblem(self, problem):
		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()
		c.execute("""INSERT INTO problems (problemId, name, category, level, solved) VALUES (?,?,?,?,?)""", (problem.problemId, problem.name, problem.category, problem.level, problem.solved) )
		conn.commit()
		conn.close()
		return problem

	def selectProblems(self):
		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()
		c.execute("""SELECT problemId FROM problems""" )
		conn.commit()
		conn.close()
		return problem

	def insertSolved(self, solved):
		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()
		c.execute("""INSERT INTO solved (userId,problemId) VALUES (?,?)""", (solved.userId, solved.problemId) )
		solved.solvedId = c.lastrowid
		conn.commit()
		conn.close()
		return solved

if __name__ == '__main__':
	db = DB()

	joao  = User("12345", "joao")
	maria = User("49876", "maria")

	joao = db.insertUser(joao)
	maria = db.insertUser(maria)

	uri1001 = Problem(1001, "facil demais", "iniciante", 1, 24)
	uri1001 = db.insertProblem(uri1001)

	for user in db.getUsers():
		user.userId