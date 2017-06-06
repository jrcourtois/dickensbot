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

page = [""]
articles = {}
indice = 0
title = ""
rePar = re.compile(r"==.*==")
reTitle= re.compile(r"\{\{(.*)\|1=(.*?)\}\}")
reDate = re.compile(r"(\d+\s.*?\s201.).*\d+\:\d\d\s\(CES?T\)$")
for line in liste.splitlines():
	l = line
	if rePar.match(l):
		indice += 1
		page.insert(indice, l + "\n") 
	else:
		if (page[indice]):
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
		try:
			txt  = p.getWikiText()
			if (txt.find("{{Article supp")>-1):
				appSupp += "\n#{{/supp|" + m.group(1) + "|" + m.group(2) + "|" + time.strftime("%d/%m/%Y") + "}}"
			elif (txt.find("{{Article cons")>-1):
				appCons += "\n#{{/cons|" + m.group(1) + "|" + m.group(2) + "|" + time.strftime("%d/%m/%Y") + "}}"
			else:
				newProps += "\n" + line
		except:
			print("**********************************page not exists")

print("***********************************")
print("Supp")
supp.edit(appendtext=appSupp,bot=True)
print(appSupp)
print("***********************************")
print("Cons")
cons.edit(appendtext=appCons,bot=True)
print(appCons)
print("***********************************")
prop.edit(text=newProps, summary="added last propositions",bot=True)
print(newProps)
t = ""
for a in page:
	t += a + "\n"

t = re.sub(r"\n\n+","\n\n", t)
disc.edit(text=t,bot=True, summary="avertissement de suppressions archivés")
