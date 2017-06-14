# -*- coding: utf8 -*-
from Analysis import Analysis
from wikitools.page import Page
from Site import site
import urllib.request, urllib.parse, urllib.error


SITE_JR = "http://www.jrcourtois.net/wiki/"

print("Modeles")
try:
	models = urllib.request.urlopen(SITE_JR + "models.wiki")
	modelPage = Page(site,"Utilisateur:DickensBot/Modeles")
except urllib.error.HTTPError as e:
	print ("models.wiki was missing")


modelPage.edit(text = models.read().decode("utf8"), summary = "Mise à jour", bot=True)

def printPageFromFile(page, fileName):
	try:
		s = urllib.request.urlopen(SITE_JR + "arch/" + fileName)
	except urllib.error.HTTPError as e:
		print("File not found: %s" % fileName)
		return
	if s.getcode() != 200:
		return
	lines = s.readlines()
	print(("%s => %s" % (fileName,catName)))
	ret = "{|class='wikitable sortable'\n"
	ret += "!Titre!!Nb links!!Nb pages traduites!!tpl !! en page !! de page !! es page !! models !! admisssible \n"
	for l in lines:
		ret += "|-\n"
		ret += l.decode("utf8")
	ret +="|-\n"
	ret+= "|}"
	p = Page(site, page + "/analysis")
	p.edit(text = ret, summary=str(len(lines)) + " articles à adopter", bot=True)

a = Analysis(site)
a.run()


YEAR = [2014, 2015, 2016, 2017]
MONTH = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
# orphelins 
for y in YEAR:
	m =1
	for mon in MONTH:
		catName = "Catégorie:Article orphelin depuis %s %d" %(mon, y)
		fileName= "orph_%d-%02d.arch" % (y, m)
		printPageFromFile(catName, fileName)
		catName = "Catégorie:Wikipédia:Tentative d'adoption en %s %d" %(mon, y)
		fileName= "tent_%d-%02d.arch" % (y, m)
		printPageFromFile(catName, fileName)
		m += 1



