# -*- coding: utf8 -*-
import urllib.request, urllib.parse, urllib.error
import json

server = "https://petscan.wmflabs.org/?min_redlink_count=1&minlinks=&edits%5Bflagged%5D=both&outlinks_no=&sparql=&wikidata_prop_item_use=&sitelinks_yes=&langs_labels_no=&language=fr&search_wiki=&maxlinks=&wikidata_source_sites=&templates_yes=&common_wiki=auto&ores_prediction=any&larger=&combination=subset&page_image=any&cb_labels_any_l=1&output_compatability=quick-intersection&cb_labels_yes_l=1&edits%5Banons%5D=both"
apres = "&labels_yes=&active_tab=tab_output&referrer_name=&min_sitelink_count=&source_combination=&search_query=&wikidata_item=no&referrer_url=&manual_list=&templates_any=&regexp_filter=&output_limit=&links_to_all=&pagepile=&sitelinks_no=&wikidata_label_language=&cb_labels_no_l=1&outlinks_yes=&show_redirects=both&ores_prob_from=&max_age=&wpiu=any&search_max_results=500&doit=Do%20it!&before=&after=&links_to_any=&labels_any=&labels_no=&langs_labels_any=&langs_labels_yes=&ores_type=any&negcats=&interface_language=en&max_sitelink_count=&templates_no=&sortby=none&project=wikipedia&links_to_no=&subpage_filter=either&smaller=&manual_list_wiki=&sitelinks_any=&sortorder=ascending&ns%5B0%5D=1&edits%5Bbots%5D=both&depth=0&common_wiki_other=&ores_prob_to=&outlinks_any=&format=json"
class QuickIntersection:
	def __init__(self,cats):

		self.url = server + "&categories=" + urllib.parse.quote("\n".join(cats).encode("utf8")) + apres
		self.count = 0
		self.pages = {}
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


