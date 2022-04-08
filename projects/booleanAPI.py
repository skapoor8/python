yin = True
yang = False

meanings = {
	"Yin": "Dao",
	"Yang": "Dao",
	"True": "Yin",
	"False": "Yang",	
	"Enlightenment": "Dao",
	"Good": "Yin",
	"Bad": "Yang",
	"Hashtag": "Dao",
}

def source(word)
	if dao(word):
		return True
	else if dao(word) == False:
		return False
	else:
		return source(next(word))

def addMeaning(word, meaning):
	meanings[word] = meaning

def hasMeaning(word):
	return meanings[word]


# daoObject
class Dao:
	yin = True
	yang = False
	meaning = {
		"Yin": "Dao",
		"Yang": "Dao",
		"True": "Yin",
		"False": "Yang",	
		"Enlightenment": "Dao",
		"Good": "Yin",
		"Bad": "Yang",
		"Hashtag": "Dao",
	}

	def notDao(word, meaning):
		meanings[word] = meaning

	def Dao(word):
		return meanings[word]

# daoAPI
def next(word):
	return meanings[word]

# Truth Object
class Truth:
	def isTrue(word):
		return boolean(word)

	def isFalse(word):
		return boolean(word)

	def boolean(word):
		return Dao.Dao(boolean(word))
