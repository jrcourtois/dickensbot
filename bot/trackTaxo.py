# -*- coding: utf8 -*-
from Site import site
from  Tools import printProgress
import re
from wikitools.page import Page


def parseTaxo(t):
	print(t)
	projet = Page(site, "Projet:" + t  + "/Articles orphelins")
	lines = projet.getWikiText().decode("utf8").split("\n")
	allCats = {}

	res = ""
	i = 0
	for p in lines:
		printProgress(i, len(lines))
		i+=1
		m = re.match(r'\#\ \[\[(.*)\]\]$', p)
		if m:
			a = m.group(1)
			page = Page(site, a)
			if "Taxobox" in page.getWikiText():
				p += " (T)"
		res += p + "\n"

	projet.edit(text=res, summary="bot: ajout des pages taxoboxées", bot=True)

parseTaxo("Biologie cellulaire et moléculaire")
parseTaxo("Biologie")
parseTaxo("Botanique")
parseTaxo("Zoologie")
parseTaxo("Entomologie")
