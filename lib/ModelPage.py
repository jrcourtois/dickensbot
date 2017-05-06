# -*- coding: utf8 -*-
import Site
import Tools
import re
from wikitools import api
from wikitools import Page
from pprint import pprint

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
		print "Found links : "+ str(len(self.frenchLinks)) + "/" + str(len(self.getLinks())) + " for " + self.title.encode("utf8")
		return translatedLinks

	def getTranslatedTemplate(self):
		json = self.getJson()
		ret = u"<noinclude>{{Création automatique|DickensBot}}</noinclude>\n"
		ret+= u"{{Méta palette de navigation\n"
		try:
			ret+= u"| titre = " + self.getLink(json["title"],json["links"]) + "\n"
		except:
			ret+= u"|titre = " + self.title + "\n"
		ret+= u"| modèle = Palette " + self.modele + "\n"
		try:
			if json["image"]:
				ret+= u"| image = " + self.getLink(json["image"][0],json["links"])  + "\n"

		except:
			print "Problem with image"
		for t in sorted(json["groups"]):
			g = json["groups"][t]
			ret += self.getLinksTranslated(t,g,json["links"])
		ret += u"}}\n<noinclude>{{Documentation palette}}\n[[Catégorie:Palette de navigation]]</noinclude>\n"

		return ret.encode("utf8")

	def getLinksTranslated(self, cnt, grp, tab):
		try:
			ret = u" | groupe" + cnt + u" = " + self.getLink(grp["title"],tab)  + u"\n" 
		except:
			print "gLT:problem with : " 
			pprint(grp)
			ret = u" | groupe" + cnt + u" = " + self.getLink("list",tab)  + u"\n" 
		if grp["sub"]:
			ret += " | liste" + cnt + u" = {{Méta palette de navigation sous-groupe\n"
			for t in sorted(grp["list"]):
				g = grp["list"][t]
				ret += self.getLinksTranslated(t,g,tab)
			ret += "}}\n"
			return ret
		phrase = grp["list"]
		phrase = re.sub(r"___L___\s*\*+", "\n | ",phrase).decode("utf8")
		try:
			ret = ret.decode("utf8")
		except:
			print "PROBLEM"
			pprint(ret)
		ret += " | liste"
		ret += cnt
		ret += u" = {{liste éléments"
		ret += self.getLink(phrase,tab)
		ret += "\n}}\n"
		return ret


	def getLink(self, phrase, tab):
		for key in re.findall(r"__l:\d+__", phrase):
			try:
				phrase = phrase.replace(key, self.getTranslatedLink(tab[key].decode("utf8")))
			except:
				print "Problem with " + tab[key]
		phrase = phrase.replace("___L___", "")
		return phrase

	def getTranslatedLink(self, oLink):
		oLink = oLink.replace("[[","").replace("]]", "")
		if oLink.split(":")[0] == "Image":
			return "[[" + oLink + "]]"
		if oLink.split(":")[0] == "File":
			return "[[" + oLink + "]]"
		link = oLink.split("|")
		aff = u""
		if self.translatedLinks.has_key(link[0]):
			try:
				if len(link)>1:
					aff = u"|" + link[1]
				return u"[[" + self.translatedLinks[link[0]]  + aff + "]]"
			except:
				print "problem with : " + link[0]
		try:
			if len(link)>1:
				aff = link[1]
			else:
				aff = link[0]
			return getLinkLg(link[0], aff, self.lg)
#			return u"{{lien|trad="+link[0]+u"|texte="+ aff + u"|langue="+self.lg+u"|fr=" + link[0] + u"}}"
		except:
			print "Probelm with: " + link[0]
			return "[[" + oLink + "]]"

def getLinkLg(enLink, texte, lguage):
	return u"{{lien|langue=%s|trad=%s|fr=%s|texte=%s}}" % (lguage, enLink, enLink, texte)


class EnglishModelPage(ItlPage):
	"""A page which is a model"""
	def __init__(self, title, translation):
		ItlPage.__init__(self, "en", title, translation)

	

	def oldTranslatedTemplate(self):
		try:
			text = self.getWikiText().decode("utf8")
		except:
			text = self.getWikiText()
			print "Got an exception on decoding utf8"
			pprint(text)
		for link in re.findall(r"\[\[.*?\]\]", text):
			m = re.match(r"\[\[(.*)\|(.*)\]\]",link)
			if (m):
				if  self.translatedLinks.has_key(m.group(1)):
					text = text.replace(link, "[[" + self.translatedLinks[m.group(1)] + "|" + m.group(2) + "]]")
				else:
					text = text.replace(link, getLinkLg(m.group(1), m.group(2),"en"))
					#text = text.replace(link, "{{lien|trad="+m.group(1)+"|texte="+m.group(2)+"|lang=en|trad="+m.group(1)+u"}}")
			else:
				m = re.match(r"\[\[(.*?)\]\]", link)
				if self.translatedLinks.has_key(m.group(1)):
					text = text.replace(link, "[[" + self.translatedLinks[m.group(1)] + "]]")
				else:
					text = text.replace(link, getLinkLg(m.group(1), m.group(1),"en"))
					#text = text.replace(link, "{{lien|trad="+m.group(1)+"|texte="+m.group(1)+"|lang=en|trad="+m.group(1)+u"}}")

		text = text.replace("Navbox", u"M\xe9ta palette de navigation")
		text = text.replace("name", u"mod\xe8le")
		text = text.replace("body", "liste")
		text = text.replace("title", "groupe")
		text = text.replace("\n*", " SEPSEPSEP ")
		text = re.sub(r"SEPSEPSEP", r"\n   | ",re.sub(r"(liste\d+)+\s*\=\s*(.*)", r"\1 = {{liste elements\n   | \2\n}}", text)).replace("elements",u"\xe9l\xe9ments")
		return text
	def getJson(self):
		json = {}
		text = self.getWikiText()#.decode("utf8")
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
			if not tree.has_key(g[0]):
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
			if sub.has_key(t[0]):
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
			text = self.getWikiText().decode("utf8")
		except:
			text = self.getWikiText()
			print "Got an exception on decoding utf8"
			pprint(text)
		text = re.sub(r"\[(.*?)\|.*?\]", r"[\1]",text)
		for a in self.translatedLinks:
			text = text.replace(a, self.translatedLinks[a])
		text = text.replace("Navigationsleiste", u"M\xe9ta palette de navigation")
		text = text.replace("name", u"mod\xe8le")
		text = text.replace("BILD", "image")
		text = text.replace("INHALT", "liste")
		text = text.replace("TITEL", "titre")
		text = text.replace("\n*", " SEPSEPSEP ")
		text = re.sub(r"SEPSEPSEP", r"\n   | ",re.sub(r"(liste\d+)+\s*\=\s*(.*)", r"\1 = {{liste elements\n   | \2\n}}", text)).replace("elements",u"\xe9l\xe9ments")
#		text = re.sub(r"^\s*|\s*$", "", text,flags=re.MULTILINE)
		return text


class ModelPage(Page):
	def __init__(self, title):
		Page.__init__(self, Site.site, title)
		self.name = re.sub(".*Palette ", "", self.title)
		print self.name

	def parseLinks(self):
		print self
		for p in self.getLinks():
			page = Page(Site.site, p)
			if page.exists and page.namespace == 0:
				print p
				Tools.addPalette(page,self.name)
	
