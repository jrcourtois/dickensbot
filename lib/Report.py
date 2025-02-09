# -*- coding: utf8 -*-
from OrphanPage import OrphanPage

class Report(object):

	def __init__(self):
		self.models_f = open('files/models.wiki', 'w')
		self.desorphan_f = open("files/adopte.wiki", "w")
		self.orphan_2_f = open("files/orphan2.wiki", "w")

		self.models = {}
		self.withModel = 0
		self.adopted_cnt = 0
		self.doModels = False

	def parsePage(self, p):
		page = OrphanPage(p, self.doModels)
		if page.toAdopt():
			self.adopted_cnt += 1
			self.desorphan_f.write("# [[" + p + "]]\n") 
			return
		if page.getNbLinks ==2:
			self.orphan2_f.write("# [[" + p + "]]\n") 
		if self.doModels:
			if page.getNbItlModels()>0:
				self.withModel += 1
				for l in page.itlModels:
					for model in page.itlModels[l]:
						key = l + ":" + model["title"]
						if key in self.models:
							self.models[key] += [page.title]
						else:
							self.models[key] = [page.title]

	def printReport(self):

		print(str(self.withModel) + " page(s) with model")  
		print(str(len(self.models)) + " model(s)") 
		print(str(self.adopted_cnt) + " orphans adopted") 


		self.models_f.write("{|class='wikitable sortable'\n")
		self.models_f.write("!title!!Nb using!!articles\n")
		self.models_f.write("|-\n")
		i = 0
		for m in self.models:
			print(m.encode("utf8"))
			if (len(self.models[m]) > 1): 
				self.models_f.write("|[[:" + m + "]] ||" + str(len(self.models[m])) + "||")
				for a in self.models[m]:
					self.models_f.write("[[" + a + "]], ")
				self.models_f.write("\n|-\n")
		self.models_f.write("|}")
		self.models_f.close()

