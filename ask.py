import web
from web import form

render = web.template.render('templates/')

urls = ('/', 'index',
	'/credits', 'credits')

EASTER_EGGS = ["seahorse", "seahorses",] 
IDIOTS = ["JessicaSimpson", "ParisHilton", "lindsaylohan", "kanyewest", "glennbeck", "GovMikeHuckabee", "JoeLieberman",
	"katyperry", "algore", "KarlRove", "TilaTequila", "SarahPalinUSA"]
		
app = web.application(urls, globals())


myform = form.Form( 
	form.Textbox("term"),) 
	
class credits:
	def GET(self):
		return render.credits()

class index:
	def GET(self): 
		form = myform()
		return render.formtest(form)

	def POST(self): 
		form = myform() 
		if not form.validates(): 
			return render.formtest(form)
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
				intersection = filter(lambda l:l in x.text.rsplit(" "), _getList(term))
				if len(intersection) > 0:
					return x
				return None
			elif x is None:
				intersection = filter(lambda l:l in y.text.rsplit(" "), _getList(term))
				if len(intersection) > 0:
					return y
				return None
			else:
				terms = _getList(term)
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
		result = reduce(_compare, statuses)
		if result is None:
			return render.howiroll(myform())
		return render.result(result, term, myform())
			
	def handleEasterEgg(self, term):
		if term == "seahorse" or term == "seahorses":
			return render.cups(myform())

if __name__ == "__main__":
	app.run()
