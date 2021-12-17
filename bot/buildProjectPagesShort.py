# -*- coding: utf8 -*-
from Site import site
from Tools import getFrenchDate
import re
import time
from ProjectCategory import ProjectCategory
from wikitools.page import Page

date = getFrenchDate().replace(" ", "_")
reDate = re.compile(".*DickensDate\((.+?)\)", re.MULTILINE)

projets = Page(site, "Utilisateur:DickensBot/Projets-Courts")
lines = projets.getLinks()
allCats = {}

nbError = 0

for p in lines:
	m = re.match(r'Projet:(.*)\/Articles orphelins', p)
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

for w in sorted(allCats, key=allCats.get, reverse=True):
	print(w.catName, allCats[w], w.getFilteredCount())
	w.savePageShort()

