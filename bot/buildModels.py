# -*- coding: utf8 -*-
from Site import site
from ModelPage import EnglishModelPage
from ModelPage import ModelPage
import re
from wikitools.page import Page

def getPalette(f, templateName, county, state):

	c = county.replace("Comté de ", "").replace("Comté d'", "")

	m = re.findall(r".*seat\s*=\s*(.*)\s", f)

	if (len(m) == 1):
		seat = m[0]

	m = re.findall(r".*map_image\s*=\s*(.*)\s", f)

	if (len(m) == 1):
		map = m[0]

	t = re.sub(r"ments\s+\|", "ments", f)

	t = re.sub(r"liste(\d+)\s", r"contenu\1", t)

	t = re.sub(r"groupe(\d+)\s=.*City.*", r"titre\1 = Villes", t)
	t = re.sub(r"groupe(\d+)\s=.*Township.*", r"titre\1 = Townships", t)
	t = re.sub(r"groupe(\d+)\s=.*CDP.*", r"titre\1 = CDPs", t)
	t = re.sub(r"groupe(\d+)\s=.*communities.*", r"titre\1 = Secteurs non constitués en municipalité", t)
	t = re.sub(r"groupe(\d+)\s=.*Ghost.*", r"titre\1 = Villages fantômes", t)
	t = re.sub(r"groupe(\d+)\s=.*Footnotes.*",  r"titre\1 = Notes", t)
	t = re.sub(r"fr=(.*?),\s(.*?)\|", r"fr=\1 (\2)|", t)
	t = re.sub(r"=.*populated place.*", "= {{liste éléments| ‡ Ce(s) endroit(s) partagent du territoire dans un/des comté(s) adjacent(s)", t)


	header = "{{Palette Comté américain\n"
	header+= " | modèle      = %s\n" % (templateName)
	header+= " | comté       = %s\n" % (county)
	header+= " | état        = %s\n" % (state)
	if map:
		header+= " | carte       = %s\n" % map

	if seat:
		header+= " | siège       = %s\n"% seat

	header+= t[t.find("| titre"):t.find("<noinclude")]
	footer = "<noinclude>{{Documentation palette}}\n"
	footer+= "{{DEFAULTSORT:%s (%s)}}\n" % (county, state)
	footer+= "[[Catégorie:Palette Comté des États-Unis|%s (%s)]]\n" % (c, state)
	footer+= "[[Catégorie:Modèle %s]]</noinclude>" % (state)
	return header + footer

def buildPalette(englishTemplate, county, state):
	m = "%s (%s)" % (county, state)
	palette = "Palette " + m
	model = "Modèle:Palette " + m
	page = EnglishModelPage(t,m)


	if m != "":
		template = page.oldTranslatedTemplate().replace("–", "-")
		texte = getPalette(template, palette, county, state)
		print(texte)

		p = Page(site, model)
		p.edit(text = texte, summary="Créé par un bot, merci d'aider à la traduction",bot=True)
		return p.title


templates = open("templates.txt").readlines()
counties = open("counties.txt").readlines()

i=0
res = []
cError = 0
for t in templates:
	print((t.strip()))
	try:
		#frenchPalette = buildPalette(t.strip().decode("utf8"), counties[i].strip().decode("utf8"), "Iowa")
		frenchPalette = "Modèle:Palette %s (%s)" % (counties[i].strip().decode("utf8"),"Iowa")

		p = ModelPage(frenchPalette)
		p.parseLinks()
	except RuntimeError as e:
		print(("Error on %s : %s", (counties[i].strip(), e)))
		cError += 1
		if cError > 2:
			break
	except KeyboardInterrupt:
		print("Fin par control C")
		break
	i+=1