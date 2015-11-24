import os
import sqlite3
from user import User
from problem import Problem
from solved import Solved
from uri import Uri

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATABASE_FILE = FILE_PATH + "/../database.db"

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
		c.execute("""DELETE FROM solved where userId=?""", (user.userId,))
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

	def getContestProblems(self, users, categories):
		conn = sqlite3.connect(DATABASE_FILE)
		c = conn.cursor()

		if len(users) == 1:
			users.append(users[0])

		c.execute("""DROP VIEW IF EXISTS getProblems""")
		c.execute("""CREATE VIEW getProblems AS
					 SELECT solved.problemId, COUNT(solved.problemId) AS usersSolved
					 FROM solved 
					 WHERE solved.userId IN %s
					 GROUP BY (solved.problemId)""" % str(tuple(users)))

		c.execute("""DROP VIEW IF EXISTS sortProblems""")
		c.execute("""CREATE VIEW IF NOT EXISTS sortProblems AS
					 SELECT problems.*, getProblems.usersSolved 
					 FROM problems
					 LEFT JOIN getProblems ON problems.problemId=getProblems.problemId
					 ORDER BY category, usersSolved ASC, level ASC, solved DESC""")

		problems = []
		for category, quantity in categories:
			q = c
			print category
			q.execute("""SELECT sortProblems.problemId, sortProblems.name
						 FROM sortProblems
						 WHERE sortProblems.category = '%s'""" % category)
			
			for problem in q.fetchmany(quantity):
				problems.append({'problemId' : problem[0], 'name' : problem[1]})

		conn.commit()
		conn.close()

		return problems

	def updateJudge(self):
		print 'Updating judge...'

		uri = Uri()
		problems = uri.getProblems()

		print len(problems), " problems."

		self.insertProblems(problems)

	def updateUser(self,user):
		print '\nUpdating user %s...' % user.name

	 	uri = Uri(user)
	 	problems = uri.getProblems()
	 	
	 	print "%d problems." % len(problems)
	 	
	 	self.insertSolveds(problems)

	def updateUsers(self):
		print 'updating users'

		users = self.getUsers()

		for user in users:
			self.updateUser(user)

if __name__ == '__main__':
	db = DB()
	db.updateJudge()
	# db.updateUsers()
