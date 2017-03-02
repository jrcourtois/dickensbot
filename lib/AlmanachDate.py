# -*- coding: utf8 -*-
import re
from wikitools import api
from wikitools import category
from Site import site
import datetime 

MONTH = [u"janvier", u"février", u"mars", u"avril", u"mai", u"juin", u"juillet", u"août", u"septembre", u"octobre", u"novembre", u"décembre"]

WEEK = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


class AlmanachDate :
	def __init__(self, d, m, y):
		self.d = d
		self.m = m
		self.year = y
		self.m_num = MONTH.index(m) + 1
		self.decade = self.year[0:3] + "0"
		self.y_num = int(self.year)
		if self.d == "1er":
			self.d_num = 1
		else:
			self.d_num = int(self.d)

		self.date = "%s %s %s" % (d, m, y)
		day = datetime.date(self.y_num, self.m_num, self.d_num)
		self.dow = WEEK[day.timetuple().tm_wday]
		self.doy = day.timetuple().tm_yday
		self.sdate = '"' + self.date + '"'

		# Récupérations des articles liés
		params = {'action':'query', 'list':'search', 'srsearch':self.sdate, 'srlimit' : 1000}
		request = api.APIRequest(site, params)
		result = request.query(False)
		self.articles = result['query']['search']
		print u"%s : %d pages " % (self.date, len(self.articles))

	def findBirth(self, s):
		m = re.search(u"n.*? (\d\d? \w+ \d+)", s, re.U)
		if (m):
			if m.group(1) != self.date :
				return m.group(1)
		m = re.search(u"(\d\d? \w+ \d+).+?(\d\d? \w+ \d+)", s, re.U)
		if (m):
			if m.group(1) != self.date :
				return m.group(1)
		return "XXX"

	def findDeath(self, s):
		m = re.search(u"m.*? (\d\d? \w+ \d+)", s, re.U)
		if (m):
			if m.group(1) != self.date :
				return m.group(1)
		m = re.search(u"(\d\d? \w+ \d+).+?(\d\d? \w+ \d+)", s, re.U)
		if (m):
			if m.group(2) != self.date :
				return m.group(2)
		return ""

	def findOther(self, s):
		m = re.search(u"créé", s, re.U)
		if (m):
			return u"Création"
		m = re.search(u"sort", s, re.U)
		if (m):
			return u"Sortie"
		return False

	def getWikiPage(self):
		ret = u"{{Création automatique|DickensBot}}\n"
		ret+= "{{Infobox Jour|%s|%s|%s}}\n" % (self.d_num, self.m_num, self.y_num)
		ret+= "\n"
		ret+= u"Le %s '''%s %s %s''' est le %d{{e}} jour de l'année [[%s]]." % (self.dow, self.d, self.m, self.y_num, self.doy, self.y_num)
		ret+= "\n"
		if len(self.birthArray) > 0:
			ret+= "\n== Naissances ==\n"
			ret+= self.getBirths()
		if len(self.deathArray) > 0:
			ret+= u"\n== Décès ==\n"
			ret+=self.getDeaths()

		ret+= u"\n== Autres événements ==\n"
		ret+= self.getOthers()
		ret+= self.getLinked()

		ret+= "\n== Voir aussi ==\n"
		ret+= "* [[%s %s]] et [[%s %s]]\n" % (self.d,self.m,self.m,self.y_num)
		 
		ret+= u"\n{{Portail|années %s}}\n" % (self.decade)
		return ret

	def parseAndCompare(self, almMonth):
		self.birthArray = {}
		self.deathArray = {}
		self.otherArray = {}
		self.linked = []
		self.unlinked = []
		self.snippets = {}
		for p in self.articles:
			snipp = re.sub("<.*?>", "", p['snippet'])
			self.snippets[p['title']] = snipp
			if p['title'] in almMonth.birth:
				self.birthArray[p['title']] = self.findDeath(snipp)
				continue
			if p['title'] in almMonth.death:
				self.deathArray[p['title']] = self.findBirth(snipp)
				continue
			if self.findOther(snipp):
				self.otherArray[p['title']] = self.findOther(snipp)
				continue
			if p['title'] in almMonth.linkedPage:
				self.linked.append(p['title'])
			else:
				self.unlinked.append(p['title'])
	def printSummary(self):
		print "%s : %d born, %d died, %d connected, %d others" % (self.date, len(self.birthArray), len(self.deathArray),len(self.otherArray), len(self.linked) + len(self.unlinked))

	def getBirths(self):
		ret = ""
		for b in self.birthArray:
			if self.birthArray[b] == "":
				ret+= u"* '''[[%s]]''', \n" % b
			else:
				ret+= u"* '''[[%s]]''' (mort le %s), \n" % (b, self.birthArray[b])
			ret+= u"<!-- %s -->\n" % self.snippets[b]
		return ret

	def getDeaths(self):
		ret = ""
		for b in self.deathArray:
			ret+= u"* '''[[%s]]''' (né le %s), \n" % (b, self.deathArray[b])
			ret+= u"<!-- %s -->\n" % self.snippets[b]
		return ret

	def getOthers(self):
		ret = ""
		for b in self.otherArray:
			ret+= u"* [[%s]] ''(%s)''\n" % (b, self.otherArray[b])
			ret+= u"<!-- %s -->\n" % self.snippets[b]
		return ret

	def getLinked(self):
		ret = ""
		for b in self.linked:
			ret+= u"* [[%s]]" % b
			ret+= u"<!-- %s -->\n" % self.snippets[b]
		return ret
	def getAll(self):
		ret = ""
		for b in self.otherArray:
			ret+= u"* [[%s]] ''(%s)''\n" % (b, self.otherArray[b])
			ret+= u"<!-- %s -->\n" % self.snippets[b]
		for b in self.linked:
			ret+= u"* [[%s]]\n" % b
			ret+= u"<!-- %s -->\n" % self.snippets[b]
		for b in self.unlinked:
			ret+= u"* [[%s]]\n" % b
		return ret

	def hasOther(self):
		return (len(self.linked) + len(self.unlinked) + len(self.otherArray) ) > 0



class AlmanachMonth:
	def __init__(self, m, y):
		self.month = "%s %s" % (m, y)
		self.m = m
		self.y = y
		# Récupération des articles liés au mois en question
		params = {'action':'query', 'bltitle' : self.month.title(), 'list':'backlinks','blnamespace':'0', 'blfilterredir':'all', 'bllimit' : 5000}
		r = api.APIRequest(site,params)
		result = r.query(False)
		self.linkedPage = []
		for p in result['query']['backlinks']:
			self.linkedPage.append(p['title'])
		print u"%d pages linked to %s" % (len(self.linkedPage), self.month)
		# Récupération des articles liés à la catégorie du mois de naissance
		month_birth = u"Catégorie:Naissance en " + self.month
		cat = category.Category(site, month_birth) 
		self.birth = cat.getAllMembers(True)
		print u"%d people born in %s" % (len(self.birth), self.month)
		# Récupération des articles liés à la catégorie du mois de décès
		month_death = u"Catégorie:Décès en " + self.month
		cat = category.Category(site, month_death) 
		self.death = cat.getAllMembers(True)
		print u"%d people died in %s" % (len(self.death), self.month)

	def getNum(self):
		return MONTH.index(self.m) + 1

		
