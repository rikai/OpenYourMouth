OpenYourMouth
=============

Open Source Recipes from the Jupiter Broadcasting community


Using the webserver
-------------------

If you have the flask and markdown python modules installed, running the webserver
is as simple as

    $ ./runserver.py

and point your browser to http://localhost:8000/

Otherwise, use virtualenv.

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ ./runserver

Testing
-------

As yet, there is no deliciousness test for the recipes.
You'll just have to try them yourselves!

Webserver and python checks can be run with

    $ pep8 *.py && ./testserver.py
