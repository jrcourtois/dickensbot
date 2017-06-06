# -*- coding: utf8 -*-
from wikitools.page import Page
import Site
import urllib.request, urllib.parse, urllib.error
import re

print("Adoption")
adopte = urllib.request.urlopen("http://www.jrcourtois.net/wiki/adopte.wiki")
i=0
for l in adopte:
	i+=1
	m = re.match(br"# \[\[(.*)\]\]", l)
	if m:
		title = m.group(1).decode("utf8")
		adopted = Page(Site.site, title)
		oldTxt = adopted.getWikiText()
		txt = re.sub(r"\{\{[O|o]rph.*?\}\}\n?", "", oldTxt)
		if txt == oldTxt:
			print ("Bandeau absent")
		else:
			print (adopted.edit(txt, summary = "Article adopte !",bot=True))


