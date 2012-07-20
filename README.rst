Photostash
==========


API Endpoints
-------------

A version of the api is running on at http://photostash.herokuapp.com/api/v1/ that you can make api requests against.


Albums
~~~~~~

**List**

List all albums in the system::

  GET /albums/

Parameters:

  - **name** - Name of the album you would like you filter on.

Response::

  Status: 200 OK

  {
    "meta": {
      "limit": 20,
      "next": null,
      "offset": 0,
      "previous": null,
      "total_count": 2
    },
    "objects": [
      {
        "id": "1",
        "name": "family",
        "resource_uri": "/api/v1/albums/1/"
      },
      {
        "id": "2",
        "name": "vacation",
        "resource_uri": "/api/v1/albums/2/"
      },
    ]
  }


**Create**

Create a new album::

  POST /albums/

Input:

  - **name** - *Required* The name you would like to give the album.

Example::

  {"name": "my-photos"}

Response::

  Status: 201 Created

  {
    "id": "1",
    "name": "my-photos",
    "resource_uri": "/api/v1/albums/1/"
  }


**Get**

  GET /albums/1/

Response::

  Status: 200 OK

  {
    "id": "1",
    "name": "my-photos",
    "resource_uri": "/api/v1/albums/1/"
  }


**Update**

  PUT /albums/1/

Input:

  - **name** - *Required* The name you would like to give the album.

Example::

  {"name": "my-new-photos"}

Response::

  Status: 202 Accepted

  {
    "id": "1",
    "name": "my-new-photos",
    "resource_uri": "/api/v1/albums/1/"
  }


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
