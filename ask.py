import web
from web import form
from settings import EASTER_EGGS, IDIOTS, GOOGLE_ANALYTICS_KEY

render = web.template.render('templates/')

urls = ('/', 'index',
	'/credits', 'credits')

app = web.application(urls, globals())

myform = form.Form( 
	form.Textbox("term"),) 
	
class credits:
	def GET(self):
		return render.credits(GOOGLE_ANALYTICS_KEY)

class index:
	def GET(self): 
		form = myform()
		return render.formtest(form, GOOGLE_ANALYTICS_KEY)

	def POST(self): 
		form = myform() 
		if not form.validates(): 
			return render.formtest(form, GOOGLE_ANALYTICS_KEY)
		else:
			term = form['term'].value
			if term in EASTER_EGGS:
				return self.handleEasterEgg(term)
			return self.handleSearch(term)

	def handleSearch(self, term):
		import twitter
		import random
		api = twitter.Api()
		statuses = []
		for i in random.sample(IDIOTS, 3):
			tmp = api.GetUserTimeline(i, count=50)
			if tmp is not None:
				statuses = statuses + tmp
		def _compare(x, y):
			if y is None and x is None:
				return None
			elif y is None:
				intersection = filter(lambda l:l in x.text.rsplit(" "), terms)
				if len(intersection) > 0:
					return x
				return None
			elif x is None:
				intersection = filter(lambda l:l in y.text.rsplit(" "), terms)
				if len(intersection) > 0:
					return y
				return None
			else:
				intersectionx = filter(lambda l:l in x.text.rsplit(" "), terms)
				intersectiony = filter(lambda l:l in y.text.rsplit(" "), terms)
				sizeDiff = len(intersectionx) - len(intersectiony)
				if sizeDiff > 0:
					return x
				elif sizeDiff < 0:
					return y
				else:
					if len(intersectionx) == len(intersectiony) and len(intersectionx) == 0:
						return None
					elif x.created_at > y.created_at:
						return x
					else:
						return y
			return None

		def _getList(term):
			from thesaurus import thesaurus
			t = thesaurus()
			return t.getAll(term)
		terms = _getList(term)
		print terms
		result = reduce(_compare, statuses)
		if result is None:
			return render.howiroll(myform(), GOOGLE_ANALYTICS_KEY)
		return render.result(result, term, myform(), GOOGLE_ANALYTICS_KEY)
			
	def handleEasterEgg(self, term):
		if term == "seahorse" or term == "seahorses":
			return render.cups(myform(), GOOGLE_ANALYTICS_KEY)

# needed to run on Dreamhost (need great hosting?  Sign up with my referral code - http://www.dreamhost.com/r.cgi?66120)
#web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)

if __name__ == "__main__":
	app.run()
