# -*- coding: utf8 -*-
from ModelPage import EnglishModelPage
from ModelPage import ModelPage
from wikitools import Page
from Site import site
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("template")
parser.add_argument("modele")
parser.add_argument("--noPrint", action='store_true', dest='noPrint')
parser.add_argument("--noEdit", action='store_true', dest='noEdit')
args = parser.parse_args()

t = args.template.decode("utf8")
m = args.modele.decode("utf8")

page = EnglishModelPage(t,m)


if m != "":
	p = Page(site, u"Modèle:Palette "+ m)
	template = page.getTranslatedTemplate().decode("utf8")
	template = template.replace(u"–", u"-")
	if args.noPrint == False:
		print page.oldTranslatedTemplate()
	if args.noEdit == False:
		p.edit(text = template.encode("utf8"), summary=u"Créé par un bot, merci d'aider à la traduction",bot=True)
		print u"Page : " + p.title + u" créée"

else :
	print page.getTranslatedTemplate()
#modele = ModelPage(p.title)

#modele.parseLinks()


