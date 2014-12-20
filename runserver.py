#!/usr/bin/env python

import os
import markdown
from io import open
from flask import Flask, Markup, abort, render_template

app = Flask("OpenYourMouth")


@app.route('/')
def index():
    all_recipes = get_recipes()
    categories = all_recipes.keys()
    categories.sort()
    return render_template('index.html',
                           recipes=all_recipes,
                           categories=categories)


@app.route('/<category>/')
def category(category):
    try:
        some_recipes = get_recipes(category)
    except IOError:
        abort(404)
    except FileNotFoundError:
        # python3
        abort(404)

    if not some_recipes:
        abort(404)

    return render_template('category.html',
                           recipes=some_recipes[category],
                           category=category)


# BUG: Doesn't account for subcategories properly. i.e. Bacon
@app.route('/<category>/<recipe>/')
def recipe(category, recipe):
    try:
        recipe_html = get_recipe(category, recipe)
    except IOError:
        abort(404)
    except FileNotFoundError:
        # python3
        abort(404)

    if not recipe_html:
        abort(404)

    return render_template('recipe.html',
                           recipe_title=recipe,
                           content=recipe_html)


# Usage:
#  get_recipes()
#  get_recipes("category")
#
#  returns a dict of categories -> recipe list
#  if no category is specified, return all categories
#
#  Notes:
#    For now, we read from the filesystem directly
#    there is no database or cache.
def get_recipes(category=None):
    if not category:
        category = '.'

    # dict comprehensions are cool!
    # os.walk returns a list of tuples of (path, directories, files)
    d = {w[0].lstrip('./'): w[2]        # category -> listofrecipes
         for w in os.walk(category)      # watch for leading './'
         if w[2]                         # Ignore empty directories
         and '.md' in w[2][0]}           # Use directories with recipes

    for category in d.keys():
        d[category] = map(lambda r: r.rstrip('.md'), d[category])

    return d


# Usage:
#  get_recipe("category", "recipe")
#
#  returns the html Markup of the specified recipe
def get_recipe(category, recipe):
    path = os.path.join(category, recipe + '.md')

    # Note: no effort has been made to give consistent errors
    # For now, callers should catch
    #   IOError in python2
    #   FileNotFoundError in python3
    with open(path) as md_f:
        md = md_f.read()

    html = Markup(markdown.markdown(md))
    return html


if __name__ == '__main__':
    host = os.environ.get('HOST', '::')
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host=host, port=port, debug=debug)
