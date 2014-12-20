#!/usr/bin/env python
import unittest
from runserver import *


class TestRecipeInternalAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_all_recipes(self):
        all_recipes = get_recipes()
        self._check_get_recipes(all_recipes)

    def test_get_bacon_recipes(self):
        bacon_recipes = get_recipes('Bacon')
        self._check_get_recipes(bacon_recipes)

    def test_get_bacon_british(self):
        bacon_recipes = get_recipes('Bacon/British')
        self._check_get_recipes(bacon_recipes)

    def test_get_bacon_snacks(self):
        bacon_recipes = get_recipes('Bacon/Snacks')
        self._check_get_recipes(bacon_recipes)

    def test_get_breakfast_recipes(self):
        breakfast_recipes = get_recipes('Breakfast')
        self._check_get_recipes(breakfast_recipes)

    def _check_get_recipes(self, R):
        self.assertIsInstance(R, dict, R)
        for category in R.keys():
            recipes = R[category]
            self.assertIsInstance(recipes, list, category)
            for recipe in recipes:
                self.assertNotIn('.md', recipe,
                                 "{}:{}".format(category, recipe))

    def test_get_fried_eggs_recipe(self):
        fried_eggs = get_recipe('Eggs', 'FriedEggs')
        self._check_get_recipe(fried_eggs)

    def test_get_curry_udon(self):
        sauce = get_recipe('Sauces', 'AlfredoSauce')
        self._check_get_recipe(sauce)

    def _check_get_recipe(self, R):
        self.assertIsInstance(R, Markup, R)
        # TODO: self.assertIsDelicious(R)

if __name__ == '__main__':
    unittest.main()
