# -*- coding: utf8 -*-
from wikitools import Page
from wikitools import NoPage
import Site
from ModelPage import ItlPage
from wikitools import api
import Tools

adm = "Catégorie:Tous les articles dont l'admissibilité est à vérifier"
homo = "Catégorie:Homonymie"
class OrphanPage(Page):
	"""An orphan page"""

	def __init__(self, title):
		Page.__init__(self, Site.site,title)
		params = {'action':'query', 'titles' : title, 'prop':'langlinks'}
		request = api.APIRequest(Site.site, params)
		result = request.query(False)
		self.title = title
		self.interwikiLinks = []
		self.nblinks = self.__getNbLinks(Site.site, title)
		self.models = self.__getLinks(Site.site, title, '10')
		self.itlModels = {}
		self.itlLinks = {}
		for p in result['query']['pages']:
			if 'langlinks' in list(result['query']['pages'][p].keys()):
				self.interwikiLinks = result['query']['pages'][p]['langlinks']
		for l in self.interwikiLinks:
			s = Site.getKnownSite(l['lang'])
			# I know the language
			if (s):
				self.itlLinks[l['lang']] = self.__getLinks(s, l['*'], '0')
				self.itlModels[l['lang']] = self.__getLinks(s, l['*'], '10')

	def toAdopt(self):
		print (("%s has %d links" % (self.title, self.getNbLinks())))
		try:
			if self.getNbLinks() > 2:
				return True
			if self.isHomo():
				print((self.title.decode("utf8") + " is an homonyme page"))
				return True
		except NoPage as e:
			print("No page found")
			print((self.title))
		return False

	def getNbItlModels(self):
		i = 0
		for l in self.itlModels:
			i+= len(self.itlModels[l])
		return i
	def getNbModels(self):
		return len(self.models)
	def getNbTrads(self):
		return len(self.interwikiLinks)
	def getNbEnLinks(self):
		return len(self.itlLinks)
	def getNbLinks(self):
		return self.nblinks

	def __getNbLinks(self, site, l):
		if not type(l) is str:
			l = l.decode('utf8')
		params = {'action' : 'query', 'bltitle' : l, 'list' : 'backlinks', 'blnamespace' : '0', 'blfilterredir':'all'}
		r = api.APIRequest(site,params)
		result = r.query(False)
		pages = {}
		for p in result['query']['backlinks']:
			if "redirect" in list(p.keys()):
				if "redirlinks" in list(p.keys()):
					for r in p["redirlinks"]:
						pages[r["pageid"]] = True
			else:
				pages[p["pageid"]] = True
		return len(pages)
			
	def __getLinks(self, site, l, ns):
		if not type(l) is str:
			l = l.decode('utf8')
		params = {'action':'query', 'bltitle' : l, 'list':'backlinks','blnamespace':ns, 'blfilterredir':'nonredirects'}
		r = api.APIRequest(site, params)
		result = r.query(False)
		return result['query']['backlinks']
		
	def toCheck(self):
		p = Page(Site.site, self.title)
		return adm in p.getCategories()
	def isHomo(self):
		p = Page(Site.site, self.title)
		return homo in p.getCategories()

	def getFrenchPages(self):
		self.itlPages = []
		for l in self.itlModels:
			for p in self.itlModels[l]:
				self.itlPages.append(ItlPage(l,p['title'],""))
		self.pages = {}
		for l in self.itlLinks:
			self.pages[l] = []
			for p in self.itlLinks[l]:
				t = Tools.getFrenchPage(Site.getKnownSite(l),p['title'])
				if t: 
					self.pages[l].append(t)


