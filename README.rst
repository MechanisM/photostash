Photostash
==========


Deploying
---------
Photostash was created to be deployed to Heroku_.

Clone the repo from github_::

$ git cline git://github.com/seanbrant/photostash.git

Then push it up to a new Heroku app::

$ cd photostash
$ heroku create
$ git push heroku master

Once deployed you can create the datatbase::

$ heroku run python manage.py syncdb


Configuring
-----------

Photostash is configured using environment variables. Use the `heroku config` command::

$ heroku config:add VARIABLE=value

Required settings:

  - `SECRET_KEY`: A secret key for this particular Django installation. Used to provide a seed in secret-key hashing algorithms. Set this to a random string -- the longer, the better.
  - `AWS_ACCESS_KEY_ID`: Your Amazon Web Services access key, as a string.
  - `AWS_SECRET_ACCESS_KEY`: Your Amazon Web Services secret access key, as a string.

Optional settings:

  - `DEBUG`: A boolean that turns on/off debug mode. Only use this if you really, really need to.


Developing
----------

Create a virtualenv::

$ virtualenv photostash

Install the projects requirements::

$ pip install -r photostash/requirements.txt

Create the database::

$ python photostash/manage.py syncdb

Start up the server::

$ python photostash/manage.py runserver

Running the test suite::

$ python photostash/manage.py test


.. _Heroku: https://heroku.com
.. _github: https://github.com/seanbrant/photostash
