# -*- coding: utf8 -*-
from ModelPage import EnglishModelPage
from ModelPage import ModelPage
from wikitools.page import Page
from Site import site
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("template")
parser.add_argument("modele")
parser.add_argument("--noPrint", action='store_true', dest='noPrint')
parser.add_argument("--noEdit", action='store_true', dest='noEdit')
args = parser.parse_args()

t = args.template
m = args.modele

page = EnglishModelPage(t,m)


if m != "":
	p = Page(site, "Modèle:Palette "+ m)
	template = page.getTranslatedTemplate()
	template = template.replace("–", "-")
	if args.noPrint == False:
		print((page.oldTranslatedTemplate()))
	if args.noEdit == False:
		p.edit(text = template, summary="Créé par un bot, merci d'aider à la traduction",bot=True)
		print(("Page : " + p.title + " créée"))

else :
	print((page.getTranslatedTemplate()))
#modele = ModelPage(p.title)

#modele.parseLinks()


