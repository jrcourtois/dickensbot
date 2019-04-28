# -*- coding: utf8 -*-
from wikitools.page import Page
from wikitools import api
import re
import urllib.request, urllib.parse, urllib.error
import time
import Site
import sys

def addModele(txt, modele):
	tab = txt.split("\n")
	newTxt = ""
	l = 0
	if "Taxobox" in txt:
		return modele + "\n" + txt
	for line in tab:
		if line.startswith("{") and line.endswith("}"):
			newTxt += line + "\n"
		else:
			return newTxt + modele + "\n" + "\n".join(tab[l:])
		l+=1
def isFromCat(cats, catStart):

	for cat in cats:
		if cat.rfind(catStart) > -1:
			return True
	return False

def isOrphanCat(l):
	return isFromCat(l,"Article orphelin/Liste complète")

def getPortail(l):
	ret = []
	for cat in l:
		if cat.find("Portail") > -1:
			ret.append(cat)
	return ret
month = {'01': 'janvier', '02':"février", "03" : "mars", "04" : "avril", "05":"mai","06":"juin",
			'07':'juillet', '08':'août', '09':'septembre','10':'octobre', '11':'novembre', '12':'décembre'}

def getFrenchDate():
	return month[time.strftime("%m")] + " " + time.strftime("%Y")


def getBotTxt(fromTxt, toTxt):
	toTxt  = toTxt.replace("== Category intersection ==", "<!--")
	toTxt  = toTxt.replace("== Results ===", "-->")
	if fromTxt.find("<!-- BEGIN BOT SECTION -->")>-1:
		return re.sub(r"(.*\<\!\-\- BEGIN BOT SECTION \-\-\>).*(\<\!\-\- END BOT SECTION \-\-\>.*)",r"\1\n"+toTxt+r"\n\2", fromTxt, flags=re.S)

	else:
		return "<!-- BEGIN BOT SECTION -->\n" + toTxt + "\n<!-- END BOT SECTION -->"
def printProgress(indice, top):
	progress = (float(indice)*100 / top)
	sys.stdout.write("Progress: %g %%   \r" % (progress) )
	sys.stdout.flush()

def addPalette(page, title, adopt = False):
	txt = page.getWikiText()
	match = re.search(r"\{\{[P|p]alette.(.+?)\}\}", txt) 
	if match:
		for elem in match.group(1).split("|"):
			if elem == title:
				print(("deja la"))
				return
		txt = re.sub(r"\{\{([P|p]alette).(.*)\}\}", r"{{\1|\2|"+title+"}}",txt)
	else:
		if re.search(r"\{\{[P|p]ortail.*\}\}", txt):
			txt = re.sub(r"(\{\{[P|p]ortail.*\}\})", "{{Palette|"+title+"}}\n" + r"\1",txt)
		else:
			print(("pas de portail"))
	if (adopt):
		txt = re.sub(r"\{\{[O|o]rph.*?\}\}\n?", "", txt)

	commentaire = "Ajout de la palette: ''"+ title + "''"
	page.edit(txt, summary=commentaire,bot=True)


def getFrenchPage(site, page):
	params = {'action':'query', 'prop':'langlinks', 'titles':page}
	request = api.APIRequest(site, params)
	try:
		result = request.query(False)
	except urllib.error.HTTPError:
		print("Unable to handle request %s" % params)
		return None
	for p in result['query']['pages']:
		links = []
		if 'langlinks' in result['query']['pages'][p]:
			links = result['query']['pages'][p]['langlinks']
		for l in links:
			if (l['lang'] == 'fr'):
				if type(l['*']) is str:
					pageTitle = l['*']
				else:
					pageTitle = l['*'].decode("utf8")
				print("getFrenchPage : %s" % pageTitle)
				return Page(Site.site, pageTitle)
	return None
def setOrphan(p):
	ret = ""
	new = p.getWikiText()
	if len(new) == 0:
		return "empty"
	if new.find("{{en cours}}") > -1:
		return "en cours"
	if new.find("{{nobots}}") > -1:
		return "nobots"
	if new.lower().find("{{portail") == -1:
		 ret = "------ NO PORTAIL ----------"

	new = addModele(new, "{{orphelin|date="+getFrenchDate()+"}}")
	p.edit(new, nocreate="True", summary="article orphelin", bot=True)
	return ret

def appendCat(page, cat, key):
	cats = page.getCategories()
	if not isFromCat(cats, cat):
		print((page.title))
		txt = page.getWikiText()
		if key:
			catKey = cat + "|" + key
		else:
			catKey = cat
		if txt.endswith("\n"):
			catTxt = "[[Catégorie:"+catKey+"]]\n"
		else:
			catTxt = "\n[[Catégorie:"+catKey+"]]\n"
		page.edit(appendtext=catTxt.encode("utf8"), summary = "[bot] Ajout de la catégorie : [["+cat+"]]".encode("utf8"), bot=True)

def setOrphanIfNeeded(p):
	cat = p.getCategories()
	if p.isHomo():
		return 0
	if ( not isOrphanCat(cat)):
		setOrphan(p)
		return 1
	return 0
