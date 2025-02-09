# -*- coding: utf8 -*-
from wikitools import wiki
# create a Wiki object
site = wiki.Wiki("https://fr.wikipedia.org/w/api.php")
# login - required for read-restricted wikis
b = site.login("DickensBot", "le bot a un nouveau mot de passe")
en_site = wiki.Wiki("https://en.wikipedia.org/w/api.php")

wikt = wiki.Wiki("https://fr.wiktionary.org/w/api.php")

known_language = ["en", "es", "de"]
def getKnownSite(l):
	if l in known_language:
		return wiki.Wiki("https://"+l+".wikipedia.org/w/api.php")
	return None
