import sqlite3
from user import User
from problem import Problem
from solved import Solved
from uri import Uri

DATABASE_FILE = "./../database.db"

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
		c.execute("""INSERT OR REPLACE INTO problems (problemId, name, category, level, solved) VALUES (?,?,?,?,?)""", (problem.problemId, problem.name, problem.category, problem.level, problem.solved) )
		conn.commit()
		conn.close()
		return problem

	def insertProblems(self, problems):
		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()
		for problem in problems:
			c.execute("""INSERT OR REPLACE INTO problems (problemId, name, category, level, solved) VALUES (?,?,?,?,?)""", (problem.problemId, problem.name, problem.category, problem.level, problem.solved) )
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
		c.execute("""INSERT OR REPLACE INTO solved (userId,problemId) VALUES (?,?)""", (solved.userId, solved.problemId) )
		solved.solvedId = c.lastrowid
		conn.commit()
		conn.close()
		return solved


	#issue: return only those that have been inserted
	def insertSolveds(self, solveds):
		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()

		for i,solved in enumerate(solveds):
			c.execute("""INSERT OR REPLACE INTO solved (userId,problemId) VALUES (?,?)""", (solved.userId, solved.problemId) )
			solveds[i] = c.lastrowid
		conn.commit()
		conn.close()
		return solveds

def updateJudge():
	print 'updating judge'
	db = DB()

	uri = Uri()
	db.insertProblems(uri.getProblems())

def updateUsers():
	print 'updating users'
	db = DB()
	users = db.getUsers()

	for user in users:
		print 'updating user %s' % user.name
	 	uri = Uri(user)
	 	db.insertSolveds(uri.getProblems())		

def teste():
	conn = sqlite3.connect(DATABASE_FILE)
	c = conn.cursor()
	c.execute("""SELECT SUM(resolvidos) as total
				from solved 
				 """)
	solved.solvedId = c.lastrowid
	conn.commit()
	conn.close()


if __name__ == '__main__':
	# updateJudge()
	# updateUsers()

