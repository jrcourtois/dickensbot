# -*- coding: utf8 -*-
from wikitools.category import Category
import Site
from OrphanPage import OrphanPage
import argparse
import Tools


parser = argparse.ArgumentParser("To parse a category")
parser.add_argument("catName")
args = parser.parse_args()
catName = args.catName

cat = Category(Site.site,catName) 

tab = cat.getAllMembers(True)

trt = open("files/trt.wiki")

treated = trt.read().splitlines()

trt.close()

orp0 = open("files/orp0.wiki","a+")
orp1 = open("files/orp1.wiki","a+")
orp2 = open("files/orp2.wiki","a+")
trt = open("files/trt.wiki","w")


try:
	i = 0
	for p in tab:
		i+=1
		print(p, file=trt)
		if (p not in treated):
			Tools.printProgress(i, len(tab))
			page = OrphanPage(p)
			if page.getNbLinks()==0:
				print(p,file=orp0)
			if page.getNbLinks()==1:
				print(p,file=orp1)
			if page.getNbLinks()==2:
				print(p,file=orp2)
except:
	print ("INTERROMPU")
orp0.close()
orp1.close()
orp2.close()
trt.close()

orphan0 = open("files/orp0.wiki").read().splitlines()
orphan1 = open("files/orp1.wiki").read().splitlines()
orphan2 = open("files/orp2.wiki").read().splitlines()


print("== Orphelins ==")
print("''Orphelins : %d''" % len(orphan0))
print("{{colonnes|taille=30|")
for p in orphan0:
	print("* [[%s]]" % p)
print("}}")
print("== 1 seul lien ==")
print("''1 seul lien : %d''" % len(orphan1))
print("{{colonnes|taille=30|")
for p in orphan1:
	print("* [[%s]]" % p)
print("}}")
print("== 2 liens ==")
print("''2 liens : %d''" % len(orphan2))
print("{{colonnes|taille=30|")
for p in orphan2:
	print("* [[%s]]" % p)
print("}}")
print("Non orphelins : %d sur %d" % (i - len(orphan0) - len(orphan1) - len(orphan2), i))



