# -*- coding: utf8 -*-
import urllib.request, urllib.parse, urllib.error
import json

server = "http://petscan.wmflabs.org/?lang=fr&project=wikipedia&"
default_p = "&depth=12&max=30000&start=0&format=json&get_count=1&sparse=1&redirects=&callback="


class QuickIntersection:
	def __init__(self,cats):

		self.url = server + "cats=" + urllib.parse.quote("\n".join(cats).encode("utf8")) + default_p
		try:
			self.json = urllib.request.urlopen(self.url).read()
			res = json.loads(self.json)
			self.count = res['pagecount']
			self.pages = res['pages']
		except:
			print("Unable to load: " + self.url)
			self.json = ""
			self.count = 0
			self.pages = []

	def getJson(self):
		return self.json
	def getUrl(self):
		return self.url

	def getPages(self):
		return self.pages
	def getPageCount(self):
		return self.count


