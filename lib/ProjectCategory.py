# -*- coding: utf8 -*-
from wikitools.page import Page
from QuickIntersection import QuickIntersection
import Site
import re

reStart = re.compile(".*start: (\d+) pages", re.MULTILINE)
reDate = re.compile(".*date\((.+)\)", re.MULTILINE)

class ProjectCategory:
	def __init__(self,p,date):
		self.catName = p
		self.date = date
		self.portail = "Portail:" + p + "/Articles liés"
		allOrphans= QuickIntersection(["Article orphelin", self.portail])
		adm = QuickIntersection(["Article orphelin", self.portail, "Tous les articles dont l'admissibilité est à vérifier"])
		self.getOldPage()
		self.count = allOrphans.getPageCount()
		self.pages = allOrphans.getPages()
		self.admissibles = []
		for admissible in adm.getPages():
			self.admissibles.append(admissible)
		self.subProject = []
		self.parentProject  = None
		self.orph = []
		self.tent = []
		self.tentLast = []
		self.orphLast = []
		self.adopt = []


	def getFilteredCount(self):
		return len(self.pages)

	def getCount(self):
		return self.count

	def getStartCount(self):
		if self.startCount == -1:
			return self.getCount()
		return self.startCount

	def getCurrentCount(self):
		return len(self.orph) + len(self.tent)

	def getWikiLink(self):
		return "[[Projet:" + self.catName  + "/Articles orphelins|"+self.catName+"]]"

	def getProjectPage(self):
		return self.projectPage

	def getDiscPage(self):
		return ""

	def setParent(self, parent):
		self.parentProject = parent

	def getParent(self):
		if self.parentProject:
			return self.parentProject.getWikiLink() + "\n\n"
		return "--Racine--\n\n"
	
	def hasParent(self):
		return self.parentProject != None

	def isParent(self, child):
		# same object
		if self ==child:
			return False
		# A child with no pages is not linkable
		if child.getCount() == 0:
			return
		# don't go if it ca be his father
		if child.getCount() >= self.getCount():
			return False
		if child.hasParent():
			return False
		for item in child.pages:
			if item not in self.pages:
				return False
		return True

	def setChild(self, child):
		self.subProject.append(child)

		for item in self.pages:
			if item in child.pages:
				self.pages.remove(item)
		return True
				

	def getOldLinks(self):
		ret = []
		for page in self.projectPage.getLinks():
			if page.startswith("Portail:") or page.startswith("Projet:") or page.startswith("Wikipédia:") or page.startswith("Discussion"):
				return ret
			ret.append(page)
		return ret

	def getOrphans(self):
		self.orphLast = QuickIntersection(["Article orphelin depuis " + self.date, self.portail]).getPages()
		self.tentLast = QuickIntersection(["Wikipédia:Tentative d'adoption en " + self.date, self.portail]).getPages()
		self.adopt = []
		if self.startCount != -1:
			for a in self.getOldLinks():
				if a.replace(" ","_") not in self.pages:
					self.adopt.append(a)
		self.tent =   []
		allTentatives = []
		try:
			allTentatives = QuickIntersection(["Wikipédia:Tentative d'adoption", self.portail]).getPages()
		except:
			print("No tentative found")
		for t in allTentatives:
			if t not in self.tentLast:
				self.tent.append(t)
		self.orph =   []
		for o in self.pages:
			if o not in self.orphLast and o not in allTentatives:
				self.orph.append(o)


	def getMessage(self):
		s = "\n== Articles orphelins à adopter ==\n"
		s+= "<!-- DickensDate(" + self.date + ") -->\n"
		s+= "{{adoption/message|name=%s|count=%d|previousCount=%d}}" % (self.catName, self.getCount(), self.getStartCount())
		s+= "\n~~~~"
		return s.encode("utf8")

	def getPageText(self):
		s= "=== Articles orphelins ===\n"
		s+= "{{adoption/orphelins|"+str(len(self.orph))+"}}\n"
		s+= self.getPageArray(self.orph)
		s+= "==== Orphelins depuis ce mois-ci  ====\n"
		s+= "{{adoption/orphLast|"+str(len(self.orphLast))+"}}\n"
		s+= self.getPageArray(self.orphLast)
		s+= "==== Tentative  ====\n"
		s+= "{{adoption/visited|"+str(len(self.tent))+"}}\n"
		s+= self.getPageArray(self.tent)
		s+= "==== Tentatives ce mois-ci ====\n"
		s+= "{{adoption/visitedLast|"+str(len(self.tentLast))+"}}\n"
		s+= self.getPageArray(self.tentLast)
		s+= "=== Articles traités ===\n"
		s+= "{{adoption/adopted|"+str(len(self.adopt))+"}}\n"
		#s+= self.getPageArray(self.adopt)
		return s

	def getPageArray(self, pages):
		s = ""
		for l in pages:
			if l in self.admissibles:
				s+="# ''[[" + l.replace("_", " ") + "]]''\n"
			else:
				s+="# [[" + l.replace("_", " ") + "]]\n"
		if (len(pages) > 4):
			return "{{Colonnes|taille=30|\n" + s + "}}\n"
		else:
			return s
	
	def getHeader(self):
		s = "{{Mise à jour bot|Jrcourtois|période=}}\n"
		s+= "{{adoption}}\n"
		s+= "== Liste des articles orphelins ==\n"
		s+= "{{adoption/intro|" + str(self.getCount()) +  "|" + self.catName + "}}\n"
		s+= "<!-- start: " + str(self.getStartCount()) + " pages -->\n"
		s+= "<!-- date(" + self.date + ") -->\n"
		s+= self.getArbo()
		return s

	def getArbo(self):
		s = "\n\n" + self.getParent()
		s+= "'''" + self.catName + "'''\n\n" 
		for p in self.subProject:
			s+= p.getWikiLink() + " - "
		return s + "\n\n"


	def getOldPage(self):
		self.projectPage = Page(Site.site, "Projet:" + self.catName + "/Articles orphelins")
		if self.projectPage.exists:
			self.oldText = self.projectPage.getWikiText()
			try:
				self.startCount = int(reStart.search(self.oldText).group(1))
			except:
				print("no count found")
				self.startCount = -1
			try:
				date = reDate.search(self.oldText).group(1)
			except:
				print("no date found")
				date =""
			if (date != self.date):
				self.startCount = -1
		else:
			self.oldText = ""
			self.startCount = -1
	def savePage(self):
		self.getOrphans()
		summary = "MAJ: " + str(self.getCount())
		to = self.getHeader() + self.getPageText()
		print(summary + " - " + self.catName)
		t = ProjectCategory.getBotTxt(self.oldText, to).encode("utf8")
		print(self.projectPage.title)
		self.projectPage.edit(text=t,summary = summary,bot=True)

	@staticmethod
	def getBotTxt(fromTxt, toTxt):
		if fromTxt.find("<!-- BEGIN BOT SECTION -->")>-1:
			t = re.sub(r"(.*\<\!\-\- BEGIN BOT SECTION \-\-\>).*(\<\!\-\- END BOT SECTION \-\-\>.*)",r"\1\n"+toTxt+r"\n\2", fromTxt, flags=re.S)
			return t
	
		else:
			return "<!-- BEGIN BOT SECTION -->\n" + toTxt + "\n<!-- END BOT SECTION -->"
