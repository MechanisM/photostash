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
      }
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

**Delete**

  DELETE /albums/1/

Response::

  Status: 204 No Content


Photos
~~~~~~

**List**

List all photos in the system::

  GET /photos/

Parameters:

  - **albumphotos__album** - ID of the album you want to filter on.

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
        "albumphotos": [
          "/api/v1/albumphotos/1/"
        ],
        "id": "1",
        "image": "..path..",
        "resource_uri": "/api/v1/photos/1/"
      },
      {
        "albumphotos": [
          "/api/v1/albumphotos/2/"
        ],
        "id": "2",
        "image": "..path..",
        "resource_uri": "/api/v1/photos/2/"
      },
    ]
  }


**Create**

Create a new album::

  POST /photo/

Input:

  - **image** - *Required* <filename>:<base64encoded image>

Example::

  {"image": "photo.jpg:RG8gb3IgRG8gbm90LiBUaGVyZSBpcyBubyB0cnku"}

Response::

  Status: 201 Created

  {
    "albumphotos": [
      "/api/v1/albumphotos/1/"
    ],
    "id": "1",
    "image": "..path..",
    "resource_uri": "/api/v1/photos/1/"
  }


**Get**

  GET /photos/1/

Response::

  Status: 200 OK

  {
    "albumphotos": [
      "/api/v1/albumphotos/1/"
    ],
    "id": "1",
    "image": "..path..",
    "resource_uri": "/api/v1/photos/1/"
  }


**Delete**

  DELETE /photos/1/

Response::

  Status: 204 No Content



Album Photos
~~~~~~~~~~~~

*Album photos represent a relationship between a photo and a album.*


**List**

List all album photos in the system::

  GET /albumphotos/

Parameters:

  - **album** - ID of the album you want to filter on.
  - **photo** - ID of the photo you want to filter on.

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
        "album": "/api/v1/albums/1/",
        "id": "1",
        "photo": "/api/v1/photos/1/",
        "resource_uri": "/api/v1/albumphotos/1/"
      },
      {
        "album": "/api/v1/albums/1/",
        "id": "2",
        "photo": "/api/v1/photos/2/",
        "resource_uri": "/api/v1/albumphotos/2/"
      }
    ]
  }


**Create**

Create a new album::

  POST /albumphoto/

Input:

  - **album** - *Required* URI of the album
  - **photo** - *Required* URI of the photo

Example::

  {
    "album": "/api/v1/albums/1/",
    "photo": "/api/v1/photos/1/"
  }

Response::

  Status: 201 Created

  {
    "album": "/api/v1/albums/1/",
    "id": "1",
    "photo": "/api/v1/photos/1/",
    "resource_uri": "/api/v1/albumphotos/1/"
  }


**Get**

  GET /albumphotos/1/

Response::

  Status: 200 OK

  {
    "albumphotos": [
      "/api/v1/albumphotos/1/"
    ],
    "id": "1",
    "image": "..path..",
    "resource_uri": "/api/v1/photos/1/"
  }


**Delete**

  DELETE /albumphotos/1/

Response::

  Status: 204 No Content


.. _Heroku: https://heroku.com
.. _github: https://github.com/seanbrant/photostash
