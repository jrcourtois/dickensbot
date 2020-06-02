# -*- coding: utf8 -*-
from Analysis import Analysis
from wikitools.page import Page
from Site import site
import urllib.request, urllib.parse, urllib.error


SITE_JR = "http://www.jrcourtois.net/wiki/"

#print("Modeles")
#try:
#	models = urllib.request.urlopen(SITE_JR + "models.wiki")
#	modelPage = Page(site,"Utilisateur:DickensBot/Modeles")
#except urllib.error.HTTPError as e:
#	print ("models.wiki was missing")
#modelPage.edit(text = models.read().decode("utf8"), summary = "Mise à jour", bot=True)

def printPageFromWebSite(page, fileName):
	try:
		s = urllib.request.urlopen(SITE_JR + "arch/" + fileName)
	except urllib.error.HTTPError as e:
		print("File not found: %s" % fileName)
		return
	if s.getcode() != 200:
		print("File not found: %s" % fileName)
		return

	print(("%s => %s" % (fileName,page)))
	lines = s.readlines()
	printPageFromLines(page, lines)

def printPageFromFile(page, fileName):
	try:
		s = open("/home/jr/dev/wiki/dickensbot/files/arch/" + fileName )
	except FileNotFoundError:
		print ("%s n'existe pas" % fileName)
		return
	print(("%s => %s" % (fileName,page)))
	lines = s.readlines()
	if len(lines) == 0:
		print ("Empty file")
		return
	printPageFromLines(page, lines)	

def printPageFromLines(page, lines):
	if len(lines) == 0:
		print ("Empty file")
		return
	ret = "Il y a %d articles sur cette page et {{PAGESINCATEGORY:%s}} dans [[:Catégorie:%s]]\n" % (len(lines), page, page)
	ret+= "\n{{Utilisateur:DickensBot/analysis/entete}}\n"
	ret+= "{|class='wikitable sortable'\n"
	ret += "!Titre!!Nb links!!Nb pages traduites!!tpl !! en page !! de page !! es page !! models !! admisssible \n"
	for l in lines:
		ret += "|-\n"
		ret += l
	ret +="|-\n"
	ret+= "|}\n"
	ret+= "{{Palette Articles orphelins}}"
	p = Page(site, "Utilisateur:DickensBot/analysis/" + page )
	p.edit(text = ret, summary=str(len(lines)) + " articles à adopter", bot=True)



#a = Analysis(site)
#a.run()


YEAR = [2018,2019, 2020]
MONTH = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
# orphelins 
for y in YEAR:
	m = 1
	for mon in MONTH:
		catName = "Article orphelin depuis %s %d" %(mon, y)
		fileName= "orph_%d-%02d.arch" % (y, m)
		printPageFromFile(catName, fileName)
		catName = "Wikipédia:Tentative d'adoption en %s %d" %(mon, y)
		fileName= "tent_%d-%02d.arch" % (y, m)
		printPageFromFile(catName, fileName)
		m += 1

