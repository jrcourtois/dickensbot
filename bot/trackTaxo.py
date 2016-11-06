# -*- coding: utf8 -*-
from lib.Site import site
from  lib.Tools import printProgress
import re
import time
from lib.ProjectCategory import ProjectCategory
from wikitools import Page


def parseTaxo(t):
	print t
	projet = Page(site, u"Projet:" + t  + "/Articles orphelins")
	lines = projet.getWikiText().split("\n")
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

	projet.edit(text=res, summary=u"bot: ajout des pages taxoboxées", bot=True)

parseTaxo(u"Biologie cellulaire et moléculaire")
parseTaxo("Biologie")
parseTaxo("Botanique")
parseTaxo("Zoologie")
parseTaxo("Entomologie")
