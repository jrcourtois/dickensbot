# -*- coding: utf8 -*-
from wikitools.page import Page
import Site
import urllib.request, urllib.parse, urllib.error
import re
from wikitools.exceptions import APIQueryError

print("Adoption")
#adopte = urllib.request.urlopen("http://www.jrcourtois.net/wiki/adopte.wiki")
adopt_file = open("files/adopte.wiki")
adopte = adopt_file.readlines()
i=0
for l in adopte:
	m = re.match(r"# \[\[(.*)\]\]", l)
	if m:
		title = m.group(1)
		print (title)
		adopted = Page(Site.site, title)
		oldTxt = adopted.getWikiText()
		txt = re.sub(r"\{\{[O|o]rph.*?\}\}\n?", "", oldTxt)
		if txt == oldTxt:
			print ("Bandeau absent")
		else:
			try:
				adopted.edit(txt, summary = "Article [[Aide:Jargon_de_Wikipédia#Adopter_un_article_(rechercher)|adopté]] !",bot=True)
				i+=1
			except APIQueryError:
				print("%s has not been adopted" % title)
print ("%d article(s) ont été adopté(s)" % i)

