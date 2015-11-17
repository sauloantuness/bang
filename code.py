import web
import json
import time
from db import DB
from db import User

urls = (
	'/', 'index',
	'/user', 'user_api',  #POST
	'/users', 'users_api',
	'/contest', 'contest_api'
)

class index():
	def GET(self):
		f = open('./static/index.html', 'r')
		page = f.read()
		f.close()
		return page

class users_api():
	def GET(self):
		db = DB()
		users = []
		for user in db.getUsers():
			users.append(user.__dict__)

		return json.dumps(users)

class user_api():
	def POST(self):
		data = json.loads(web.data())
		user = User(name=data['name'], uriId=data['uriId'])
		db = DB()
		user = db.insertUser(user)
		return json.dumps(user.__dict__)

	def DELETE(self):
		data = json.loads(web.data())
		print data
		user = User(name=data['name'], uriId=data['uriId'], userId=data['userId'])
		db = DB()
		user = db.deleteUser(user)
		return json.dumps(user.__dict__)

class contest_api():
	def POST(self):
		data = json.loads(web.data())
		print data['users']
		print data['categories']

		#getContestProblems(users, categories)

		return json.dumps([{'problemId' : '1001', 'name' : 'Extremely Basic'},
						   {'problemId' : '1002', 'name' : 'Area of a Circle'},
						   {'problemId' : '1003', 'name' : 'Simple Sum'}])
		#create contest

if __name__ == '__main__':
	app = web.application(urls, globals())
	app.run()