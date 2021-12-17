# -*- coding: utf8 -*-
from wikitools import category
import time
from wikitools.page import Page
from OrphanPage import OrphanPage
import Site
import re

def parseArticle(p,output):
	o = OrphanPage(p, False)
	o.getFrenchPages()
	# titre
	output.write("| [[" + p + "]] ")
	# nb page linked
	output.write("|| " + str(o.getNbLinks()))
	# nb pages traduites
	output.write("|| " + str(len(o.interwikiLinks)))
	# tpl
	output.write("|| ")
	for m in o.itlPages:
		try:
			output.write("[[:"+m.lg+":"+m.title+"|"+m.lg+"]] :" + str(len(m.frenchLinks)) + "/" + str(len(m.getLinks())) +  "<br>")
		except:
			print(("error parsing: " + m.title))
	# en page
	i = 0
	for l in ["en", "de", "es"]:
		output.write("||")
		if l in o.pages:
			for p in o.pages[l]:
				i+=1
				output.write("[[%s|%d]], " % (p.title, i))
	# models
	output.write("||")
	if o.getNbModels() > 0:
		output.write("yes")

	# admissibile
	output.write("||")
	if o.toCheck():
		output.write ("yes")
	output.write("\n")

def parseArticleToString(p):
	o = OrphanPage(p)
	o.getFrenchPages()
	retString = ""
	# titre
	retString += "| [[" + p + "]] "
	# nb page linked
	retString += "|| " + str(o.getNbLinks())
	# nb pages traduites
	retString += "|| " + str(len(o.interwikiLinks))
	# tpl
	retString += "|| "
	for m in o.itlPages:
		try:
			retString += "[[:"+m.lg+":"+m.title+"|"+m.lg+"]] :" + str(len(m.frenchLinks)) + "/" + str(len(m.getLinks())) +  "<br>"
		except:
			print(("error parsing: " + m.title))
	# en page
	i = 0
	for l in ["en", "de", "es"]:
		retString += "||"
		if l in o.pages:
			for p in o.pages[l]:
				i+=1
				retString += "[[%s|%d]], " % (p.title, i)
	# models
	retString += "||"
	if o.getNbModels() > 0:
		retString += "yes"

	# admissibile
	retString += "||"
	if o.toCheck():
		retString +=  "yes"
	return retString


def compareCat(catName, displayName):
	cat = category.Category(Site.site,"Catégorie:" + catName) 
	tabWP = cat.getAllMembers(True)
	nbWP = len(tabWP)
	if nbWP == 0:
		print ("%s : vide " % displayName )
		return []
	tabFic = ""
	retTab =  []
	try:
		p = Page(Site.site, "Utilisateur:DickensBot/analysis/" + catName )
		tabFic = p.getWikiText()
	except Exception as e:
		print ("Comparaison impossible : %s" % catName)
	linesFic = {}
	for l in tabFic.split('\n'):
		m = re.match(r"\| \[\[(.*)\]\] \|\|", l)
		if m:
			linesFic[m.group(1)] = l
	i=0
	n=0
	for p in tabWP:
		if p in linesFic.keys():			
			i+=1
			retTab.append(linesFic[p])
		else:
			print (p)
			n+=1
			retTab.append( parseArticleToString(p))
	print ("%s : nbWP : %d, i : %d, n: %d, nbLine : %d" % (displayName, nbWP, i, n, len(linesFic.keys())))
	if i == len(linesFic.keys()) and n==0:
		return[]
	return retTab

def printPageFromLines(page, lines):
	if len(lines) == 0:
		return
	ret = "Il y a %d articles sur cette page et {{PAGESINCATEGORY:%s}} dans [[:Catégorie:%s]]\n" % (len(lines), page, page)
	ret+= "\n{{Utilisateur:DickensBot/analysis/entete}}\n"
	ret+= "{|class='wikitable sortable'\n"
	ret += "!Titre!!Nb links!!Nb pages traduites!!tpl !! en page !! de page !! es page !! models !! admisssible \n"
	for l in lines:
		if l:
			ret += "|-\n"
			ret += l + "\n"
	ret +="|-\n"
	ret+= "|}\n"
	ret+= "{{Palette Articles orphelins}}"
	p = Page(Site.site, "Utilisateur:DickensBot/analysis/" + page )
	p.edit(text = ret, summary=str(len(lines)) + " articles à adopter", bot=True)
	print ("%s : edited, %d lines" %  (page, len(lines)))


YEAR = [2019,2020,2021]
MONTH = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
#YEAR = [2021]
#MONTH = [ "septembre"]
# orphelins 
for y in YEAR:
	for mon in MONTH:
		catName = "Article orphelin depuis %s %d" %(mon, y)
		lines = compareCat(catName, "O:%s:%s" % (y,mon))
		printPageFromLines(catName, lines)
		catName = "Wikipédia:Tentative d'adoption en %s %d" %(mon, y)
		lines = compareCat(catName, "T:%s:%s" % (y,mon))
		printPageFromLines(catName, lines)

