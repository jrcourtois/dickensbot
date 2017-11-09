# -*- coding: utf8 -*-
import urllib.request, urllib.parse, urllib.error
import json

server = "http://petscan.wmflabs.org/?language=fr&project=wikipedia&"
default_p = "&depth=3ns&combination=subset&negcats=&larger=&smaller=&minlinks=&maxlinks=&before=&after=&max_age=&show_redirects=both&edits%5Bbots%5D=both&edits%5Banons%5D=both&edits%5Bflagged%5D=both&templates_yes=&templates_any=&templates_no=&outlinks_yes=&outlinks_any=&outlinks_no=&links_to_all=&links_to_any=&links_to_no=&sparql=&manual_list=&manual_list_wiki=&pagepile=&wikidata_source_sites=&subpage_filter=either&common_wiki=auto&source_combination=&wikidata_item=no&wikidata_label_language=&wikidata_prop_item_use=&wpiu=any&sitelinks_yes=&sitelinks_any=&sitelinks_no=&min_sitelink_count=&max_sitelink_count=&labels_yes=&cb_labels_yes_l=1&langs_labels_yes=&labels_any=&cb_labels_any_l=1&langs_labels_any=&labels_no=&cb_labels_no_l=1&langs_labels_no=&format=json&output_compatability=quick-intersection&sortby=none&sortorder=ascending&regexp_filter=&min_redlink_count=1&doit=Do%20it%21&interface_language=en&active_tab=tab_output"


class QuickIntersection:
	def __init__(self,cats):

		self.url = server + "categories=" + urllib.parse.quote("\n".join(cats).encode("utf8")) + default_p
		self.count = 0
		self.pages = []
		try:
			self.json = urllib.request.urlopen(self.url).read().decode('utf-8')
			res = json.loads(self.json)
		except urllib.error.URLError:
			print("Unable to load: " + self.url)
			self.json = ""
		except TypeError:
			print("erreur de typage")
		else:
			self.count = res['pagecount']
			self.pages = res['pages']

	def getJson(self):
		return self.json
	def getUrl(self):
		return self.url

	def getPages(self):
		return self.pages
	def getPageCount(self):
		return self.count


