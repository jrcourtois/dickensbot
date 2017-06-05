# -*- coding: utf8 -*-
from Site import site
from Tools import getFrenchDate
import re
import time
from ProjectCategory import ProjectCategory
from wikitools.page import Page

date = getFrenchDate().replace(" ", "_")
reDate = re.compile(".*DickensDate\((.+?)\)", re.MULTILINE)

projets = Page(site, "Projet:Mathématiques/Portails")
links = projets.getLinks()
allCats = {}

nbError = 0
for p in links:
	m = re.match(r'Portail:(.*)', p)
	if m:
		last = m.group(1)
		
		print(last)
		try:
			pc = ProjectCategory(last,date)
			allCats[pc] = pc.getCount()
		except:
			print("Unable to treat...")
			nbError += 1
			if nbError > 5:
				print("Too many errors, exiting")
				raise
		time.sleep(1)

text = ""
count = 0
for w in sorted(allCats, key=allCats.get, reverse=True):
	print(w.catName, allCats[w], w.getFilteredCount())
	#w.savePage()
	w.getOrphans()
	count+= int(w.getCount())
	text += "== Liste des articles du projet %s ==\n" % (w.catName)
	text += w.getPageText()
	time.sleep(1)

mathpage = Page(site, "Projet:Mathématiques/Articles orphelins")

t = ProjectCategory.getBotTxt(mathpage.getWikiText().decode("utf8"), text).encode("utf8")
summary = "MAJ: " + str(count)
#print summary
#print t
mathpage.edit(text=t,summary = summary,bot=True)

