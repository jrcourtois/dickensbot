# -*- coding: utf8 -*-
from Site import site
from Tools import getFrenchDate
import re
import time
from ProjectCategory import ProjectCategory
from wikitools.page import Page

date = getFrenchDate().replace(" ", "_")
reDate = re.compile(".*DickensDate\((.+?)\)", re.MULTILINE)

def addMessage(pc,title):
	return
	if pc.getFilteredCount() < 1:
		return
	discProjet = Page(site, "Discussion Projet:" + title)
	if not discProjet.exists:
		discProjet = Page(site, "Discussion Portail:" + title)
		if not discProjet.exists:
			print(title  + "No discussion page")
			return
	oldText = discProjet.getWikiText()
	try:
		date = reDate.search(oldText).group(1)
	except:
		print("no date found")
		date =""
	if date==pc.date:
		print("Message already added this month")
		return
		
	print(title + " comment added")
	try:
		discProjet.edit(appendtext=pc.getMessage(),bot=True, summary="bot - Merci d'adopter les articles orphelins")
	except Exception as e:
		print("Except:" , e)

def getLine(pc):
	line = " | " + pc.getWikiLink() + "||" + str(pc.getStartCount()) + "||" + str(pc.getCurrentCount())
	line+= "||" + str(len(pc.tentLast))
	line+= "||" + str(len(pc.orphLast))
	line+= "||" + str(len(pc.adopt))
	line+= "||" + str(len(pc.admissibles))
	return line


projets = Page(site, "Utilisateur:DickensBot/Projets")
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

report = ""
report = "{|class='wikitable sortable'\n"
report+="!Titre!!Début!! Current !! Visité !! Nouveau !! Adopté !! Admissible\n"
report+="|-\n"
for w in sorted(allCats, key=allCats.get, reverse=True):
	for child in sorted(allCats, key=allCats.get, reverse=True):
		if w.isParent(child):
			child.setParent(w)
			w.setChild(child)
	print(w.catName, allCats[w], w.getFilteredCount())
	w.savePage()
	report += getLine(w) + "\n|-\n"
	if w.getFilteredCount() > 10:
		addMessage(w, w.catName)
	time.sleep(1)

report+= "|}"

page = Page(site, "Utilisateur:DickensBot/Concours")
page.edit(text=report, summary = "MAJ", bot=True)
