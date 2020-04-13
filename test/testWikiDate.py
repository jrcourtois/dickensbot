# -*- coding: utf8 -*-
from WikiDate import WikiDate
import unittest

class RandomTest(unittest.TestCase):

	"""Test case utilisé pour tester les fonctions du module 'WikiDate'."""

	def test_getWikiPage(self):
		date = WikiDate(7,6,1980)
		self.assertTrue(type(date.getWikiPage()) is str)

if __name__ == '__main__':
    unittest.main()

