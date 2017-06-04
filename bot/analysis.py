# -*- coding: utf8 -*-
from wikitools import category
import time
from wikitools import Page
from OrphanPage import OrphanPage
import Site
import argparse
from Tools import printProgress


parser = argparse.ArgumentParser("To parse a category")
parser.add_argument("catName")
parser.add_argument("-d", default="analysis.wiki")
args = parser.parse_args()
catName = args.catName
destFile = "files/" + args.d

output = open(destFile,"a+")
start = time.time()

def parseArticle(p,output):

	o = OrphanPage(p)
	o.getFrenchPages()
	# titre
	output.write("| [[" + p + "]] ")
	# nb page linked
	output.write("|| " + str(o.getNbLinks()))
	# nb pages traduites
	output.write("|| " + str(len(o.interwikiLinks)))
	# tpl
	output.write("|| ")
	for m in o.itlPages:
		try:
			output.write("[[:"+m.lg+":"+m.title+"|"+m.lg+"]] :" + str(len(m.frenchLinks)) + "/" + str(len(m.getLinks())) +  "<br>")
		except:
			print(("error parsing: " + m.title))
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
#print "%s => %s" % (catName, destFile)
l = len(tab)
i=0
for p in tab:
	printProgress(i,l)
	parseArticle(p,output)
	i+=1
