# -*- coding: utf8 -*-
from Site import site
import re
from ModelPage import EnglishModelPage
from ModelPage import ModelPage
from wikitools.page import Page
from wikitools.exceptions import NoPage


class USCounty:

	def __init__(self, county, state):
		self._c = county
		self._s = state
		self._countyName = county.replace("Comté de ", "").replace("Comté d'", "")
		self._m = "%s (%s)" % (self._c, self._s)
		self._pName = "Palette " + self._m
		self._model = "Modèle:Palette " + self._m


	def getPalette(self, f):
		map = False
		seat = False


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
		t = re.sub(r"groupe(\d+)\s=.*Town.*", r"titre\1 = Towns", t)
		t = re.sub(r"groupe(\d+)\s=.*Village.*", r"titre\1 = Villages", t)
		t = re.sub(r"groupe(\d+)\s=.*CDP.*", r"titre\1 = CDPs", t)
		t = re.sub(r"groupe(\d+)\s=.*communit.*", r"titre\1 = Secteurs non constitués en municipalité", t)
		t = re.sub(r"groupe(\d+)\s=.*territory.*", r"titre\1 = Territoires", t)
		t = re.sub(r"groupe(\d+)\s=.*indian.*", r"titre\1 = Réserves indiennes", t)
		t = re.sub(r"groupe(\d+)\s=.*Former.*", r"titre\1 = Anciens lieux d'habitation", t)
		t = re.sub(r"groupe(\d+)\s=.*Ghost.*", r"titre\1 = Villages fantômes", t)
		t = re.sub(r"groupe(\d+)\s=.*Footnotes.*",  r"titre\1 = Notes", t)
		t = re.sub(r"fr=(.*?),\s(.*?)\|", r"fr=\1 (\2)|", t)
		t = re.sub(r"=.*populated place.*", "= {{liste éléments| ‡ Ce(s) endroit(s) partagent du territoire dans un/des comté(s) adjacent(s)", t)


		header = "{{Palette Comté américain\n"
		header+= " | modèle      = %s\n" % (self._pName)
		header+= " | comté       = %s\n" % (self._c)
		header+= " | état        = %s\n" % (self._s)
		if map:
			header+= " | carte       = %s\n" % map

		if seat:
			header+= " | siège       = %s\n"% seat

		header+= t[t.find("| titre"):t.find("<noinclude")]
		footer = "<noinclude>{{Documentation palette}}\n"
		footer+= "{{DEFAULTSORT:%s (%s)}}\n" % (self._c, self._s)
		footer+= "[[Catégorie:Palette Comté des États-Unis|%s (%s)]]\n" % (self._countyName, self._s)
		footer+= "[[Catégorie:Modèle %s]]</noinclude>" % (self._s)
		return header + footer

	def buildPalette(self, t):
		page = EnglishModelPage(t, self._m)

		template = page.oldTranslatedTemplate().replace("–", "-")
		texte = self.getPalette(template)
		print(texte)

		p = Page(site, self._model)
		p.edit(text = texte, summary="Créé par un bot, merci d'aider à la traduction",bot=True)
		return p.title

	def includePalette(self):
		frenchPalette = "Modèle:Palette %s (%s)" % (self._c, self._s)
		try:
			p = ModelPage(frenchPalette)
			p.parseLinks(["Siège de comté", self._s])
		except NoPage:
			print ("Page %s does not exist" % (frenchPalette))

