import simplejson
import urllib
from settings import THESAURUS_API_KEY as API_KEY

class thesaurus:
	def search(self, term):
		# Dreamhost defaults to Python 2.5, and String.format I guess isn't supported yet
		url = "http://words.bighugelabs.com/api/2/%s/%s/json" % (API_KEY, term,)
		#url = "http://words.bighugelabs.com/api/2/{0}/{1}/json".format(API_KEY, term,)
		result = simplejson.load(urllib.urlopen(url))
		return result
	def get(self, term, partOfSpeech="noun", resultType="ant"):
		result = self.search(term)
		try:
			pos = result.get(partOfSpeech)
			pos = pos.get(resultType)
			return pos
		except:
			return None
	def getAll(self, term):
		result = self.search(term)
		retval = []
		try:
			for a, b in result.items():
				if type(b) == "<type 'list'>":
					retval = retval + b
				else:
					for c, d in b.items():
						retval = retval + d
			return retval	
		except:
			return [term]
	
