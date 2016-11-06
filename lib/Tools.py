# -*- coding: utf8 -*-
from wikitools import Page
from wikitools import api
from pprint import pprint
import re
import urllib
import time
import Site
import sys

def addModele(txt, modele):
	tab = txt.split("\n")
	newTxt = u""
	l = 0
	for line in tab:
		if line.startswith("{") and line.endswith("}"):
			newTxt += line.decode("utf8") + "\n"
		else:
			return newTxt.encode("utf8") + modele.encode("utf8") + "\n" + "\n".join(tab[l:])
		l+=1
def isFromCat(cats, catStart):

	for cat in cats:
		if cat.rfind(catStart) > -1:
			return True
	return False

def isOrphanCat(l):
	return isFromCat(l,"Tous les articles orphelins")

def getPortail(l):
	ret = []
	for cat in l:
		if cat.find("Portail") > -1:
			ret.append(cat)
	return ret
month = {'01': 'janvier', '02':u"février", "03" : "mars", "04" : "avril", "05":"mai","06":"juin",
			'07':'juillet', '08':u'août', '09':'septembre','10':'octobre', '11':'novembre', '12':u'décembre'}

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

def addPalette(page,title):
	txt = page.getWikiText().decode("utf8")
	match = re.search(r"\{\{[P|p]alette.(.+?)\}\}", txt) 
	if match:
		for elem in match.group(1).split("|"):
			if re.match(r"" + title+ r"$",elem):
				print "deja la"
				return
		txt = re.sub(r"\{\{([P|p]alette).(.*)\}\}", r"{{\1|\2|"+title+"}}",txt)
	else:
		if re.search(r"\{\{[P|p]ortail.*\}\}", txt):
			txt = re.sub(r"(\{\{[P|p]ortail.*\}\})", "{{Palette|"+title+"}}\n" + r"\1",txt)
		else:
			print "pas de portail"
	commentaire = "Ajout de la palette: ''"+ title + "''"
	page.edit(txt.encode("utf8"), summary=commentaire.encode("utf8"),bot=True)


def getFrenchPage(site, page):
	params = {'action':'query', 'prop':'langlinks', 'titles':page}
	request = api.APIRequest(site, params)
	result = request.query(False)
	for p in result['query']['pages']:
		links = []
		if result['query']['pages'][p].has_key('langlinks'):
			links = result['query']['pages'][p]['langlinks']
		for l in links:
			if (l['lang'] == 'fr'):
				return Page(Site.site, l['*'])
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
		print page.title
		txt = page.getWikiText()
		if key:
			catKey = cat + "|" + key
		else:
			catKey = cat
		if txt.endswith("\n"):
			catTxt = u"[[Catégorie:"+catKey+"]]\n"
		else:
			catTxt = u"\n[[Catégorie:"+catKey+"]]\n"
		page.edit(appendtext=catTxt.encode("utf8"), summary = u"[bot] Ajout de la catégorie : [["+cat+"]]".encode("utf8"), bot=True)
