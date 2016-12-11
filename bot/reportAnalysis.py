# -*- coding: utf8 -*-
from Analysis import Analysis
from wikitools import Page
from Site import site
import urllib


SITE_JR = "http://www.jrcourtois.net/wiki/"

print "Modeles"
models = urllib.urlopen(SITE_JR + "models.wiki")
modelPage = Page(site,"Utilisateur:DickensBot/Modeles")
modelPage.edit(text = models.read(), summary = u"Mise à jour", bot=True)

def printPageFromFile(page, fileName):
	s = urllib.urlopen(SITE_JR + fileName)
	if s.getcode() != 200:
		print "%s does not exist !" % fileName
		return
	lines = s.readlines()
	print u"%s => %s" % (fileName,catName)
	ret = "{|class='wikitable sortable'\n"
	ret += "!Titre!!Nb links!!Nb pages traduites!!tpl !! en page !! de page !! es page !! models !! admisssible \n"
	for l in lines:
		ret += "|-\n"
		ret += l
	ret +="|-\n"
	ret+= "|}"
	p = Page(site, page + "/analysis")
	p.edit(text = ret, summary=str(len(lines)) + " articles à adopter",bot=True)

a = Analysis(site)
a.run()


YEAR = [2013, 2014, 2015, 2016]
MONTH = [u"janvier", u"février", u"mars", u"avril", u"mai", u"juin", u"juillet", u"août", u"septembre", u"octobre", u"novembre", u"décembre"]
# orphelins 
for y in YEAR:
	m =1
	for mon in MONTH:
		catName = u"Catégorie:Article orphelin depuis %s %d" %(mon, y)
		fileName= u"orph_%d-%02d.arch" % (y, m)
		printPageFromFile(catName, fileName)
		catName = u"Catégorie:Wikipédia:Tentative d'adoption en %s %d" %(mon, y)
		fileName= u"tent_%d-%02d.arch" % (y, m)
		printPageFromFile(catName, fileName)
		m += 1



