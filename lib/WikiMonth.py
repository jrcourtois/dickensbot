# -*- coding: utf8 -*-
import re
import requests
import datetime 
import urllib

from wikitools import api
from wikitools import category
from Site import site
from WikiDate import WikiDate
import Tools
import time


MONTH = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

WEEK = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

URL = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'

DICTIONNARY = {
	'P571' : "Création de %s",
	'P575' : "Découverte de %s",
	'P577' : "Publication de ''%s''",
	'P580' : "Début de %s",
	'P582' : "Fin de %s",
	'P585' : "%s"
	}

QUERY_GAL = '''PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?s ?sLabel ?code ?sDescription ?sitelink ?born ?death ?sex WHERE {
  ?s ?code "%s-%s-%sT00:00:00Z"^^xsd:dateTime.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "fr". }
  OPTIONAL { ?s wdt:P569 ?born. }
  OPTIONAL { ?s wdt:P570 ?death. }
  OPTIONAL { ?s wdt:P21 ?sex. }
  ?sitelink schema:about ?s .
}
ORDER BY ?sitelink'''

BORN_SWITCH = ["né", "née"]
DEAD_SWITCH = ["mort", "morte"]



class WikiMonth :
	def __init__(self, m, y):
		self.m = m
		self.y = y
		self.decade = str(y)[0:3] + "0"
		self.month = MONTH[m-1]
		self.allDays = []

		self.date = "%s %s" %(self.month, self.y)

		for i in range(1,32):
			try:
				d = WikiDate(i,m,y)
				time.sleep(2)
				d.buildPage()
				self.allDays.append(d)
			except:
				None

	def getLines(self, date, evts):
		if len(evts) == 0:
			return ""
		if len(evts) == 1:
			return "* [[%s]] : %s\n" % (date, evts[0])
		ret = "* [[%s]]\n" % date
		for e in evts:
			ret += "** %s\n" % e
		return ret


	def getAllDeath(self):
		ret = ""
		for d in self.allDays:
			evts = d.getDeath()
			ret += self.getLines(d.dayMonth, evts)

		if ret != "":
			return 	"\n== Décès ==\n{{catégorie détaillée|décès en %s}}\n%s" % (self.date, ret)
		return ret

	def getAllBirth(self):
		ret = ""
		for d in self.allDays:
			evts = d.getBirth()
			ret += self.getLines(d.dayMonth, evts)
		if ret != "":
			return 	"\n== Naissances ==\n{{catégorie détaillée|naissance en %s}}\n%s" % (self.date, ret)
		return ret

	def getOtherEvents(self, prefix = "* "):

		ret = ""
		
		for d in self.allDays:
			evts = d.getEvents()
			ret += self.getLines(d.dayMonth, evts)
		if ret != "":
			return 	"\n== Événements ==\n" + ret
		return ret

	def getWikiPage(self):
		ret = "{{ébauche|chronologie}}"
		ret+= "{{Création automatique|DickensBot|date=%s}}\n" % (Tools.getFrenchDate())
		ret+= "{{Infobox Mois|%s|%s}}\n" % (self.m, self.y)
		ret+= "\n"
		ret+= "Le mois de '''%s %s''' est le %d{{e}} mois de l'année [[%s]]." % (MONTH[self.m-1], self.y, self.m, self.y)
		ret+= "\n"
		ret+= self.getOtherEvents()
		ret+= self.getAllBirth()
		ret+= self.getAllDeath()
		 
		ret+= "\n{{Portail|années %s}}\n" % (self.decade)
		return ret

