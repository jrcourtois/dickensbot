	# -*- coding: utf8 -*-
from wikitools.page import Page
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

page = []
articles = {}
indice = 0
page.insert(0,"")
title = ""
rePar = re.compile(r"==.*==")
reTitle= re.compile(r"\{\{(.*)\|1=(.*?)\}\}")
reDate = re.compile(r"(\d+\s.*?\s202.).*\d+\:\d\d\s\(CES?T\)$")
for line in liste.splitlines():
	l = line
	if rePar.match(l):
		indice += 1
		page.insert(indice, l + "\n") 
	else:
		page[indice]+=  l + "\n"

	m = reTitle.search(l)
	if m:
		title = m.group(2)
		print(title)
	m = reDate.search(l)
	if m:
		if title:
			articles[title] = m.group(1)
			page[indice] = ""
			title = ""

props = prop.getWikiText()
for l in articles:
	props +="\n#{{/prop|%s|%s}}" % (l, articles[l])

lines = props.split("\n")
newProps = ""
appSupp = ""
appCons = ""

i = 0
for line in lines:
	#Tools.printProgress(i,len(lines))
	i+=1
	m = re.match(r"#.*\{\{\/prop\|(.*?)\|(.*)\}\}", line)
	if m:
		p = Page(site, "Discussion:" + m.group(1) + "/Suppression")
		txt  = p.getWikiText()
		suppMatch = re.match(r".*(A|a)rticle supprimé", txt, re.S)
		if suppMatch:
			appSupp += "\n#{{/supp|%s|%s|%s}}" % (m.group(1), m.group(2), time.strftime("%d/%m/%Y"))
		else:
			consMatch = re.match(r".*(a|A)rticle cons", txt, re.S)
			if consMatch:
				appCons += "\n#{{/cons|%s|%s|%s}}" % (m.group(1), m.group(2), time.strftime("%d/%m/%Y"))
			else:
				fusMatch = re.match(r".*(a|A)rticle fusionn", txt, re.S)
				if fusMatch:
					appCons += "\n#{{/cons|%s|%s|%s}} (FUSION)" % (m.group(1), m.group(2), time.strftime("%d/%m/%Y"))
				else:
					newProps += "\n" + line

print("***********************************")
print("Supp")
print(appSupp)
supp.edit(appendtext=appSupp,bot=True)
print("***********************************")
print("Cons")
print(appCons)
cons.edit(appendtext=appCons,bot=True)
print("***********************************")
print(newProps)
prop.edit(text=newProps, summary="added last propositions",bot=True)
t = ""
for a in page:
	t += a + "\n"

t = re.sub(r"\n\n+","\n\n", t)
disc.edit(text=t,bot=True, summary="avertissement de suppressions archivés")
