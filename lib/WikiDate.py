# -*- coding: utf8 -*-
import re
import requests
import datetime 
import urllib

from wikitools import api
from wikitools import category
from Site import site
import Tools


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

class WikiDate :
	def __init__(self, d, m, y):
		self.d = d
		self.m = m
		self.y = y
		self.decade = str(y)[0:3] + "0"
		self.month = MONTH[m-1]
		self.date = self._getStringDate(d, m, y)
		self.languages = []
		print(self.date)
		day = datetime.date(y, m, d)
		self.dow = WEEK[day.timetuple().tm_wday]
		self.doy = day.timetuple().tm_yday
		self.dayMonth =self. _getStringMonth(d,m)

		(self.allKeys, self.allDatas) = self._getArray(QUERY_GAL % (y, m, d))

	def _getStringDate(self, d,m,y):
		return "%s %s %s" % (str(d), MONTH[m-1], str(y))

	def _getStringMonth(self, d, m):
		if d == 1:
			return "1er %s" % ( MONTH[m-1])
		return "%s %s" % (str(d), MONTH[m-1])

	def _getArray(self, query):
		#print(query)
		data = requests.get(URL, params={'query': query, 'format': 'json'}).json()
		born = {}
		keys = []
		for item in data['results']['bindings']:
			key = item['s']['value']
			if key not in born:
				born[key] = {}
				born[key]['birth'] = "XXXX-XX-XX"
				born[key]['desc'] = "personnalité XXXXX"
				if 'born' in item  :
					born[key]['birth'] = item['born']['value']
				if 'death' in item  :
					born[key]['death'] = item['death']['value']
				born[key]['pers'] = item['sLabel']['value']
				if 'sDescription' in item:
					born[key]['desc'] = item['sDescription']['value']
				if 'sex' in item:
					born[key]['sex'] = item['sex']['value']
				else:
					born[key]['sex'] = ["Q6581097"]
				if 'sLabel' in item:
					born[key]['sLabel'] = item['sLabel']['value']
				if 'code' in item:
					born[key]['code'] = self.getName(item['code']['value'])
			if "fr.wikipedia" in item['sitelink']['value']:
				keys.append(key)
				born[key]['site'] = self.getName(item['sitelink']['value'])
			if "en.wikipedia" in item['sitelink']['value']:
				born[key]['en'] = self.getName(item['sitelink']['value'])
		return (keys, born)

	def getName(self, url):
		return urllib.parse.unquote(url.split("/")[-1])

	def _getSex(self, sex, switch):
		if "Q6581097" in sex:
			return switch[0]
		else:
			return switch[1]

	def _getDate(self, date):
		try:
			(y,m,d) = date.split("T")[0].split("-")
		except ValueError:	
			print (date)
			return 'date inconnue'
		if (d == 'XX') : 
			print (date)
			return 'date inconnue'
		return "le " + self._getStringDate(int(d), int(m), int(y))

	def _getSiteLine(self, elem, date, switch):
		sdate = ""
		if date != "":
			sdate = " (" + self._getSex(elem['sex'], switch) + " " + date + ")"

		link = self._getLink(elem)
		if 'link' != "":
				return "'''%s'''%s, %s" % (link, sdate, elem['desc'])
		return ""

	def _getLink(sefl, elem):
		if 'site' in elem:
			if elem['site'].replace("_", " ") == elem['sLabel']:
				return "[[%s]]" % (elem['sLabel'])
			else:
				return "[[%s|%s]]" % (elem['site'], elem['sLabel'])
		else:
			for lg in self.languages:
				if lg in elem:
					return "{{lien|trad=%s|texte=%s|langue=%s}}" % (elem[lg], elem['sLabel'], lg)
		return ""
	

	def getDeathLine(self, elem):
		return self._getSiteLine(elem, self._getDate(elem['birth']), BORN_SWITCH)

	def getBirthLine(self, elem):
		if ('death' in elem):
			return self._getSiteLine(elem, self._getDate(elem['death']), DEAD_SWITCH)
		else:
			return self._getSiteLine(elem, "", DEAD_SWITCH)


	def getAllDeath(self):
		events = self.getDeath()
		ret = ""
		if len(events) > 0:
			ret = "\n== Décès ==\n"
			for l in events:
				ret += "* %s\n" % l
		return ret

	def getDeath(self):
		ret = []
		for t in self.allKeys:
			if (self.allDatas[t]['code'] == 'P570'):
				ret.append(self.getDeathLine(self.allDatas[t]))
		return ret

	def getAllBirth(self):
		events = self.getBirth()
		ret = ""
		if len(events) > 0:
			ret = "\n== Naissances ==\n"
			for l in events:
				ret += "* %s\n" % l
		return ret

	def getBirth(self):
		ret = []
		for t in self.allKeys:
			if (self.allDatas[t]['code'] == 'P569'):
				ret.append(self.getBirthLine(self.allDatas[t]))
		return ret
		

	def getOtherEvents(self):
		events = self.getEvents()
		ret = ""
		if len(events) > 0:
			ret = "\n== Événements ==\n"
			for l in events:
				ret += "* %s\n" % l
		return ret

	def getEvents(self):
		self.unknown = []
		ret = []
		for t in self.allKeys:
			code = self.allDatas[t]['code']
			if code in DICTIONNARY:
				ret.append(DICTIONNARY[code] % (self._getLink(self.allDatas[t])))
			else:
				if code not in self.unknown:
					self.unknown.append(code)
		return ret


	def getWikiPage(self):
		ret = "{{ébauche|chronologie}}"
		ret+= "{{Création automatique|DickensBot|date=%s}}\n" % (Tools.getFrenchDate())
		ret+= "{{Infobox Jour|%s|%s|%s}}\n" % (self.d, self.m, self.y)
		ret+= "\n"
		ret+= "Le %s '''%s''' est le %d{{e}} jour de l'année [[%s]]." % (self.dow, self.date, self.doy, self.y)
		ret+= "\n"
		ret+= self.getAllBirth()
		ret+= self.getAllDeath()
		ret+= self.getOtherEvents()

		ret+= "\n== Voir aussi ==\n"
		ret+= "* [[%s %s]] et [[%s %s]]\n" % (self.d,self.month,self.month,self.y)
		 
		ret+= "\n{{Portail|années %s}}\n" % (self.decade)

		print(self.unknown)

		return ret
