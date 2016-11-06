# -*- coding: utf8 -*-
from wikitools import category
import time
from wikitools import Page
from OrphanPage import OrphanPage
import Site
import argparse
from pprint import pprint

parser = argparse.ArgumentParser("To parse a category")
parser.add_argument("catName")
parser.add_argument("-d", default="analysis.wiki")
args = parser.parse_args()
catName = args.catName.decode("utf8")
destFile = "files/" + args.d

start = time.time()

def parseArticle(p,output):

	o = OrphanPage(p)
	o.getFrenchPages()
	# titre
	output.write("| [[" + p.encode("utf8") + "]] ")
	# nb page linked
	output.write("|| " + str(o.getNbLinks()))
	# nb pages traduites
	output.write("|| " + str(len(o.interwikiLinks)))
	# tpl
	output.write("|| ")
	for m in o.itlPages:
		try:
			output.write("[[:"+m.lg+":"+m.title.encode("utf8")+"|"+m.lg+"]] :" + str(len(m.frenchLinks)) + "/" + str(len(m.getLinks())) +  "<br>")
		except:
			pprint ("error parsing: " + m.title)
	# en page
	i = 0
	for l in ["en", "de", "es"]:
		output.write("||")
		if l in o.pages:
			for p in o.pages[l]:
				i+=1
				output.write("[["+p.title.encode("utf8")+"|"+str(i)+"]], ")
	# models
	output.write("||")
	if o.getNbModels() > 0:
		output.write("yes")

	# admissibile
	output.write("||")
	if o.toCheck():
		output.write ("yes")
	
		

	output.write("\n")

cat = category.Category(Site.site,catName) 
tab = cat.getAllMembers(True)

#output = open(destFile,"a+")
output2 = open("files/analysis2.txt", "a+")

#output.write("==="+ catName.encode("utf8") + "===\n")
#output.write("{|class='wikitable sortable'\n")
#output.write("!Titre!!Nb links!!Nb pages traduites!!tpl !! en page !! de page !! es page !! models !! admissible\n")
#output.write("|-\n")

for p in tab:
	print p
	parseArticle(p,output2)
	#parseArticle(p,output)
	#output.write("|-\n")
	
#output.write("|}")

#output.write(u"[[:".encode("utf8")+catName.encode("utf8")+"|Cat]]\n")
#output.write("Total : " +str(len(tab)) + " articles\n")
#output.close()
#output2.close()

#inputFile = open("files/analysis.wiki", "r")

#p = Page(Site.site, "Utilisateur:DickensBot/Analysis")
#p.edit(text = inputFile.read(), summary="New update with "+ catName,bot=True)
