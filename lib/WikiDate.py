# -*- coding: utf8 -*-
import re
import requests
import datetime 

from wikitools import api
from wikitools import category
from Site import site


MONTH = [u"janvier", u"février", u"mars", u"avril", u"mai", u"juin", u"juillet", u"août", u"septembre", u"octobre", u"novembre", u"décembre"]

WEEK = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

URL = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'

DICTIONNARY = {
	'P571' : u"Création de %s",
	'P575' : u"Découverte de %s",
	'P577' : u"Publication de ''%s''",
	'P580' : u"Début de %s",
	'P582' : u"Fin de %s",
	'P585' : u"%s"
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

BORN_SWITCH = [u"né", u"née"]
DEAD_SWITCH = [u"mort", u"morte"]

class WikiDate :
	def __init__(self, d, m, y):
		self.d = d
		self.m = m
		self.y = y
		self.decade = str(y)[0:3] + "0"
		self.month = MONTH[m-1]
		self.date = self._getStringDate(d, m, y)
		self.languages = []
		print self.date
		day = datetime.date(y, m, d)
		self.dow = WEEK[day.timetuple().tm_wday]
		self.doy = day.timetuple().tm_yday

		(self.allKeys, self.allDatas) = self._getArray(QUERY_GAL % (y, m, d))

	def _getStringDate(self, d,m,y):
		return "%s %s %s" % (str(d), MONTH[m-1], str(y))


	def _getArray(self, query):
		print query
		data = requests.get(URL, params={'query': query, 'format': 'json'}).json()
		born = {}
		keys = []
		for item in data['results']['bindings']:
			key = item['s']['value']
			if key not in born:
				born[key] = {}
				born[key]['birth'] = "XXXX-XX-XX"
				born[key]['desc'] = u"personnalité XXXXX"
				if 'born' in item  :
					born[key]['birth'] = item['born']['value']
				if 'death' in item  :
					born[key]['death'] = item['death']['value']
				born[key]['pers'] = item['sLabel']['value']
				if 'sDescription' in item:
					born[key]['desc'] = item['sDescription']['value']
				if 'sex' in item:
					born[key]['sex'] = item['sex']['value']
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
		return url.split("/")[-1].replace("%20", " ").replace("%28", "(").replace("%29", ")")

	def _getSex(self, sex, switch):
		if "Q6581097" in sex:
			return switch[0]
		else:
			return switch[1]

	def _getDate(self, date):
		(y,m,d) = date.split("T")[0].split("-")
		return "le " + self._getStringDate(int(d), int(m), int(y))

	def _getSiteLine(self, elem, date, switch):
		sdate = ""
		if date != "":
			sdate = " (" + self._getSex(elem['sex'], switch) + " " + date + ")"

		link = self._getLink(elem)
		if 'link' != "":
				return u"* '''%s'''%s, %s\n" % (link, sdate, elem['desc'])
		return ""

	def _getLink(sefl, elem):
		if 'site' in elem:
			if elem['site'] == elem['sLabel']:
				return "[[%s]]" % (elem['site'])
			else:
				return u"[[%s|%s]]" % (elem['site'], elem['sLabel'])
		else:
			for lg in self.languages:
				if lg in elem:
					return u"{{lien|trad=%s|texte=%s|langue=%s}}" % (elem[lg], elem['sLabel'], lg)
		return ""
	

	def getDeathLine(self, elem):
		return self._getSiteLine(elem, self._getDate(elem['birth']), BORN_SWITCH)
	def getBirthLine(self, elem):
		if ('death' in elem):
			return self._getSiteLine(elem, self._getDate(elem['death']), DEAD_SWITCH)
		else:
			return self._getSiteLine(elem, "", DEAD_SWITCH)


	def getAllDeath(self):
		ret = ""
		for t in self.allKeys:
			if (self.allDatas[t]['code'] == 'P570'):
				ret += self.getDeathLine(self.allDatas[t])
		if ret != "":
			return 	u"\n== Décès ==\n" + ret
		return ret

	def getAllBirth(self):
		ret = ""
		for t in self.allKeys:
			if (self.allDatas[t]['code'] == 'P569'):
				ret += self.getBirthLine(self.allDatas[t])
		if ret != "":
			return 	u"\n== Naissances ==\n" + ret
		return ret

	def getOtherEvents(self):
		self.unknown = []
		ret = ""
		for t in self.allKeys:
			code = self.allDatas[t]['code']
			if code in DICTIONNARY:
				ret += "* " + DICTIONNARY[code] % (self._getLink(self.allDatas[t])) + "\n"
			else:
				if code not in self.unknown:
					self.unknown.append(code)
		if ret != "":
			return 	u"\n== Événements ==\n" + ret
		return ret

	def getWikiPage(self):
		ret = u"{{Création automatique|DickensBot}}\n"
		ret+= "{{Infobox Jour|%s|%s|%s}}\n" % (self.d, self.m, self.y)
		ret+= "\n"
		ret+= u"Le %s '''%s''' est le %d{{e}} jour de l'année [[%s]]." % (self.dow, self.date, self.doy, self.y)
		ret+= "\n"
		ret+= self.getAllBirth()
		ret+= self.getAllDeath()
		ret+= self.getOtherEvents()

		ret+= "\n== Voir aussi ==\n"
		ret+= "* [[%s %s]] et [[%s %s]]\n" % (self.d,self.month,self.month,self.y)
		 
		ret+= u"\n{{Portail|années %s}}\n" % (self.decade)

		print self.unknown

		return ret
