# -*- coding: utf8 -*-
import Site
import Tools
import re
from wikitools import api
from wikitools.page import Page

class ItlPage(Page):

	def __init__(self, l, title,translation):
		self.lg = l
		self.site = Site.getKnownSite(l)
		self.modele = translation
		self.translatedLinks = {}
		if self.site:
			Page.__init__(self, self.site, title)
			self.translatedLinks = self.__getTranslatedLinks()
		else:
			raise Exception("not known language site")
		
	def __getTranslatedLinks(self):
		params = {'action':'query', 'prop':'langlinks'}
		self.foundLink = 0
		translatedLinks = {}
		self.frenchLinks = []
		for page in self.getLinks():
			p = Tools.getFrenchPage(self.site,page)
			key = page
			#translatedLinks[key] = "{{lien|trad="+page+u"|lang="+self.lg+"}}"
			if p:
				translatedLinks[key] =   p.title
				self.frenchLinks.append(p)
		print(("Found links : %d/%d for %s" % (len(self.frenchLinks), len(self.getLinks()), self.title)))
		return translatedLinks

	def getTranslatedTemplate(self):
		json = self.getJson()
		ret = "<noinclude>{{Création automatique|DickensBot}}</noinclude>\n"
		ret+= "{{Méta palette de navigation\n"
		try:
			ret+= "| titre = " + self.getLink(json["title"],json["links"]) + "\n"
		except:
			ret+= "|titre = " + self.title + "\n"
		ret+= "| modèle = Palette " + self.modele + "\n"
		try:
			if json["image"]:
				ret+= "| image = " + self.getLink(json["image"][0],json["links"])  + "\n"

		except:
			print("Problem with image")
		for t in sorted(json["groups"]):
			g = json["groups"][t]
			ret += self.getLinksTranslated(t,g,json["links"])
		ret += "}}\n<noinclude>{{Documentation palette}}\n[[Catégorie:Palette de navigation]]</noinclude>\n"

		return ret.encode("utf8")

	def getLinksTranslated(self, cnt, grp, tab):
		try:
			ret = " | groupe" + cnt + " = " + self.getLink(grp["title"],tab)  + "\n" 
		except:
			print("gLT:problem with : %s" % grp )
			ret = " | groupe" + cnt + " = " + self.getLink("list",tab)  + "\n" 
		if grp["sub"]:
			ret += " | liste" + cnt + " = {{Méta palette de navigation sous-groupe\n"
			for t in sorted(grp["list"]):
				g = grp["list"][t]
				ret += self.getLinksTranslated(t,g,tab)
			ret += "}}\n"
			return ret
		phrase = grp["list"]
		phrase = re.sub(r"___L___\s*\*+", "\n | ", phrase)
		ret += " | liste"
		ret += cnt
		ret += " = {{liste éléments"
		ret += self.getLink(phrase,tab)
		ret += "\n}}\n"
		return ret

	def getLink(self, phrase, tab):
		for key in re.findall(r"__l:\d+__", phrase):
			phrase = phrase.replace(key, self.getTranslatedLink(tab[key]))
		phrase = phrase.replace("___L___", "")
		return phrase

	def getTranslatedLink(self, oLink):
		oLink = oLink.replace("[[","").replace("]]", "")
		if oLink.split(":")[0] == "Image":
			return "[[" + oLink + "]]"
		if oLink.split(":")[0] == "File":
			return "[[" + oLink + "]]"
		link = oLink.split("|")
		aff = ""
		if link[0] in self.translatedLinks:
			try:
				if len(link)>1:
					aff = "|" + link[1]
				return "[[" + self.translatedLinks[link[0]]  + aff + "]]"
			except:
				print(("problem with : " + link[0]))
		try:
			if len(link)>1:
				aff = link[1]
			else:
				aff = link[0]
			return getLinkLg(link[0], aff, self.lg)
#			return u"{{lien|trad="+link[0]+u"|texte="+ aff + u"|langue="+self.lg+u"|fr=" + link[0] + u"}}"
		except:
			print(("Problem with: " + link[0]))
			return "[[" + oLink + "]]"

def getLinkLg(enLink, texte, lguage):
	return "{{lien|langue=%s|trad=%s|fr=%s|texte=%s}}" % (lguage, enLink, enLink, texte)


class EnglishModelPage(ItlPage):
	"""A page which is a model"""
	def __init__(self, title, translation):
		ItlPage.__init__(self, "en", title, translation)

	

	def oldTranslatedTemplate(self):
		try:
			text = self.getWikiText()
		except:
			print("Got an exception on decoding utf8" % self.getWikiText())
		for link in re.findall(r"\[\[.*?\]\]", text):
			m = re.match(r"\[\[(.*)\|(.*)\]\]",link)
			if (m):
				if  m.group(1) in self.translatedLinks:
					text = text.replace(link, "[[" + self.translatedLinks[m.group(1)] + "|" + m.group(2) + "]]")
				else:
					text = text.replace(link, getLinkLg(m.group(1), m.group(2),"en"))
					#text = text.replace(link, "{{lien|trad="+m.group(1)+"|texte="+m.group(2)+"|lang=en|trad="+m.group(1)+u"}}")
			else:
				m = re.match(r"\[\[(.*?)\]\]", link)
				if m.group(1) in self.translatedLinks:
					text = text.replace(link, "[[" + self.translatedLinks[m.group(1)] + "]]")
				else:
					text = text.replace(link, getLinkLg(m.group(1), m.group(1),"en"))
					#text = text.replace(link, "{{lien|trad="+m.group(1)+"|texte="+m.group(1)+"|lang=en|trad="+m.group(1)+u"}}")

		text = text.replace("Navbox", "M\xe9ta palette de navigation")
		text = text.replace("name", "mod\xe8le")
		text = text.replace("body", "liste")
		text = text.replace("title", "groupe")
		text = text.replace("\n*", " SEPSEPSEP ")
		text = re.sub(r"SEPSEPSEP", r"\n   | ",re.sub(r"(liste\d+)+\s*\=\s*(.*)", r"\1 = {{liste elements\n   | \2\n}}", text)).replace("elements","\xe9l\xe9ments")
		return text
	def getJson(self):
		json = {}
		text = self.getWikiText()
		text = re.sub(r"\n+", " ___L___",text)
		try: 
			json["title"] = re.findall(r"title\s*\=\s*(.*?)\|", text)[0]
		except IndexError:
			json["title"] = "To change"

		json["image"] = re.findall(r"image\s*\=\s*(.*?)\|", text)
		lnum = 0
		json["links"] = {}
		for l in re.findall(r"\[\[.*?\]\]", text):
			label = "__l:"+str(lnum)+"__"
			lnum += 1
			json["links"][label] = l
			text = text.replace(l, label)
		tree = {}
		for g in re.findall(r"list(\d+)\s*\=\s*(\{\{.*?\}\})",text):
			if g[0] not in tree:
				tree[g[0]] = self.getSubGroup(g[1], {})
			else:
				return "ERROR"
		text = re.sub(r"list(\d+)\s*\=\s*(\{\{.*?\}\})", "subList\1 = __SUB__",text)
		json["groups"] = self.getSubGroup(text,tree)
		return json

	def getSubGroup(self, text,sub):
		json = {}
		for g in re.findall(r"list(\d+)\s*\=\s*(.*?)(\||\})", text):
			json[g[0]] = {'list' : g[1], 'sub' : False}
		for t in re.findall(r"group(\d+)\s*\=\s*(.*?)(\||\})", text):
			if t[0] in sub:
				json[t[0]] = { 'title' : t[1], 'list' : sub[t[0]], "sub" : True}
			else:
				json[t[0]]['title'] = t[1]
		return json
			

		

class DeutschModelPage(ItlPage):
	"""A page which is a model"""
	def __init__(self, title):
		ItlPage.__init__(self, "de", title)
	def getTranslatedTemplate(self):
		try:
			text = self.getWikiText()
		except:
			print("Got an exception on decoding utf8 %s" % self.getWikiText())
		text = re.sub(r"\[(.*?)\|.*?\]", r"[\1]",text)
		for a in self.translatedLinks:
			text = text.replace(a, self.translatedLinks[a])
		text = text.replace("Navigationsleiste", "M\xe9ta palette de navigation")
		text = text.replace("name", "mod\xe8le")
		text = text.replace("BILD", "image")
		text = text.replace("INHALT", "liste")
		text = text.replace("TITEL", "titre")
		text = text.replace("\n*", " SEPSEPSEP ")
		text = re.sub(r"SEPSEPSEP", r"\n   | ",re.sub(r"(liste\d+)+\s*\=\s*(.*)", r"\1 = {{liste elements\n   | \2\n}}", text)).replace("elements","\xe9l\xe9ments")
#		text = re.sub(r"^\s*|\s*$", "", text,flags=re.MULTILINE)
		return text

DONTLINK = ["Siège du comté", "Iowa"]

class ModelPage(Page):
	def __init__(self, title):
		Page.__init__(self, Site.site, title)
		self.name = re.sub(".*Palette ", "", self.title)

	def parseLinks(self):
		print((self.name))
		adopt = len(self.getLinks()) > 3
		for p in self.getLinks():
			if p in DONTLINK:
				print(("%s not LINKED" % p))
				continue
			page = Page(Site.site, p)
			if page.exists and page.namespace == 0:
				print(p)
				Tools.addPalette(page, self.name, adopt)
	
