import web, json

# Init our application, this is just about the most basic setup
urls = (
	'/', 'Index',
    '/list', 'List',
)

app = web.application(urls, globals())

# Open a database
db = web.database(dbn='sqlite', db='data.sqlite3')

class List:
    def GET(self):
        reqs = web.input()
        req = '1=1'
        for k in reqs:
            if k in ['CLASSIFIER', 'ID', 'METHOD', 'AUTHOR', 'PERSON', 'LOCATION'] and reqs[k] != '':
            	req += " AND " + k + " like '%" + reqs[k] + "%'"
        data = db.select('links',where=req).list()
        return json.dumps(data)

class Index:
	def GET(self):
		raise web.seeother('/static/index.html')

application = app.wsgifunc()
if __name__=="__main__":
    app.run()