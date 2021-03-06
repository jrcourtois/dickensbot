# -*- coding: utf8 -*-
import re
from wikitools.page import Page
from wikitools import api
import urllib.request, urllib.parse, urllib.error
import time

class Analysis:

	def __init__(self, site):
		self.Count = 0
		self.nbLine = 5
		self.site = site

		self.MODEL_NAME = "Utilisateur:DickensBot/Analysis"
		self.MODEL_TOP = self.MODEL_NAME + "/top"
		self.MODEL_BOTTOM = self.MODEL_NAME + "/bottom"
		self.articles = urllib.request.urlopen("http://www.jrcourtois.net/wiki/arch/last.arch").readlines()
	
	def getLinks(self, link):
	   params = {'action':'query', 'eititle' : link, 'list':'embeddedin'}
	   r = api.APIRequest(self.site,params)
	   result = r.query(False)
	   return result['query']['embeddedin']


	def getNextArticles(self, nb):
		i = 0
		ret = ""
		while i < int(nb) and self.Count + i < len(self.articles):
			ret +="|-\n"
			ret += self.articles[self.Count+i].decode("utf8")
			i+=1
		self.Count+=i
		self.nbLine = i
		return ret

	def run(self):

		links = self.getLinks(self.MODEL_TOP)
		for l in reversed(links):
			t = l['title']
			print(t)
			p = Page(self.site, t)
			lines =  p.getWikiText().splitlines()
			b_print = True
			ret = ""
			for line in lines:
				m = re.search(self.MODEL_TOP, line)
				if m:
					m = re.search(self.MODEL_TOP+"\|nb=(\d+)", line)
					if m:
						ret += line + "\n" + self.getNextArticles(m.group(1)) + "\n"
					else:
						ret += line + "\n" + self.getNextArticles(5) + "\n"
					b_print = False
				m = re.search(self.MODEL_BOTTOM, line)
				if m:
					b_print=True
				if b_print:
					ret+= line + "\n"

			p.edit(text = ret, summary=str(self.nbLine) + " articles à adopter",bot=True)
			time.sleep(1)

