import requests, json, re

forbidden_words = []

# Cree un dictionnaire de (mot, occurence) 
#strToDictCount = lambda s : {e : s.count(e) for e in s.split(" ")} # n^2

# Verifie si un caractère est autorise
isGoodChar = lambda x : x in [chr(i) for i in list(range(97, 97+26)) + list(range(65, 65+26))] or x == " "

# Verifie si un mot est autorise
isGoodWord = lambda x : len(x) >= 4 and not(x in forbidden_words) and not(False in [isGoodChar(letter) for letter in x])

# Renvoie l'url gutendex d'une page
getUrl = lambda id :  "https://www.gutenberg.org/files/{}/{}-0.txt".format(id, id)

# Renvoie la page gutendex recherchee
getResponseText = lambda id : requests.get(getUrl(id)).text.lower()

# Retire les mauvais caractères et mots
cleanText = lambda text : " ".join(filter(isGoodWord,re.split(r" |\n|\r", text)))

# Cree un dictionnaire avec les bons mots et leurs occurences
cleanTextToDico = lambda text : strToDictCount(text)

# Trie le dictionnaire par les valeurs decroissantes
sortedDicoCleanText = lambda dico : dict(sorted(dico.items(), key=lambda x:x[1], reverse=True))

# Text -> sortedDicoCleanText : global operation
textToSortedDicoCleanText = lambda text : sortedDicoCleanText(cleanTextToDico(cleanText(text)))

def strToDictCount(s : str):
	d = dict()
	txt = s.split(" ")

	for e in txt:
		if e in d:
			d[e] += 1
		else:
			d[e] = 1

	return d

body = 18

# Traitement
response = requests.get("https://gutendex.com/books/18")
  
if response.status_code == 200 :
	responseJson = response.json()
	title = responseJson["title"]
	downloads = responseJson["download_count"]
   
	text = getResponseText(body)
	dico = textToSortedDicoCleanText(text)

	#body = json.dumps((title, body, downloads, dico))
 
	#print(dico["prudent"])
	#print(dico["policy"])
	#print(dico)
	#print(body)