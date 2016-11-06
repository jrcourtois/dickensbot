# -*- coding: utf8 -*-
from wikitools import Page
from Site import site
import Tools
import re
import pprint
import time

disc =  Page(site,"Discussion utilisateur:Jrcourtois")
prop = Page(site, "Utilisateur:Jrcourtois/SuiviSuppressions/propositions")
supp = Page(site, "Utilisateur:Jrcourtois/SuiviSuppressions/suppressions")
cons = Page(site, "Utilisateur:Jrcourtois/SuiviSuppressions/conservations")

liste = disc.getWikiText()

page = [u""]
articles = {}
indice = 0
title = ""
rePar = re.compile(r"==.*==")
reTitle= re.compile(r"\{\{(.*)\|1=(.*?)\}\}")
reDate = re.compile(r"(\d+\s.*?\s201.).*\d+\:\d\d\s\(CES?T\)$")
for l in liste.splitlines():
	if rePar.match(l):
		indice += 1
		page.insert(indice, l.decode("utf8")+ "\n".decode("utf8")) 
	else:
		if (page[indice]):
			page[indice]+=  l.decode("utf8") + "\n".decode("utf8")

	m = reTitle.search(l)
	if m:
		title = m.group(2)
		print title
	m = reDate.search(l)
	if m:
		if title:
			articles[title] = m.group(1)
			page[indice] = ""
			title = ""

props = prop.getWikiText().decode("utf8")
for l in articles:
	props +="\n#{{/prop|" + l.decode("utf8") + "|" + articles[l].decode("utf8")+ "}}"

lines = props.split("\n")
newProps = u""
appSupp = u""
appCons = u""
i = 0
for line in lines:
	#Tools.printProgress(i,len(lines))
	i+=1
	m = re.match(r"#.*\{\{\/prop\|(.*?)\|(.*)\}\}", line)
	if m:
		p = Page(site, "Discussion:" + m.group(1) + "/Suppression")
		try:
			txt  = p.getWikiText()
			if (txt.find("{{Article supp")>-1):
				appSupp += u"\n#{{/supp|" + m.group(1) + "|" + m.group(2) + "|" + time.strftime("%d/%m/%Y") + "}}"
			elif (txt.find("{{Article cons")>-1):
				appCons += u"\n#{{/cons|" + m.group(1) + "|" + m.group(2) + "|" + time.strftime("%d/%m/%Y") + "}}"
			else:
				newProps += u"\n" + line
		except:
			print "page not exists"

print "----"
print "Supp"
supp.edit(appendtext=appSupp.encode("utf8"),bot=True)
print appSupp
print "----"
print "Cons"
cons.edit(appendtext=appCons.encode("utf8"),bot=True)
print appCons
print "----"
prop.edit(text=newProps.encode("utf8"), summary="added last propositions",bot=True)
print newProps
t = u""
for a in page:
	t += a + u"\n".encode("utf8")

t = re.sub(r"\n\n+","\n\n", t)
disc.edit(text=t.encode("utf8"),bot=True, summary="avertissement de suppressions archivés")
