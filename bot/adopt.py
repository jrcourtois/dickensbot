# -*- coding: utf8 -*-
from wikitools import Page
import Site
import urllib
import re

print "Adoption"
adopte = urllib.urlopen("http://www.jrcourtois.net/wiki/adopte.wiki")
i=0
for l in adopte:
	i+=1
	print l
	m = re.match(r'# \[\[(.*)\]\]', l)
	if m:
		try:
			title = m.group(1)
			adopted = Page(Site.site,title)
			txt = adopted.getWikiText()
			txt = re.sub(r"\{\{[O|o]rph.*?\}\}\n?", "", txt)
			adopted.edit(txt, summary = u"Article adopt\xe9 !".encode("utf8"),bot=True)
		except Exception as e:
			print "Except:" , e


