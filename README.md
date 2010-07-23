# CouchDB template tags for Django

[CouchDB](http://couchdb.apache.org) template tag for
[Django](http://www.djangoproject.com) includes content from any CouchDB URL
including lists, shows, and views.

## Configuration

Specify your primary CouchDB server with the ``COUCHDB_SERVER`` variable in your
Django settings.py. If ``COUCHDB_SERVER`` isn't set, the template tag will
default to ``http://localhost:5984``.

## Usage

Load the template library in your template:

    {% load couchdb %}

The first argument is a path relative to your CouchDB server. For example, the
following example outputs ``{"couchdb":"Welcome","version":"0.10.0"}``.

    {% couchdb / %}

Optional query parameters are specified using keyword arguments. For example,
the following example includes the output of a CouchDB list with documents
included:

    {% couchdb /mydb/_design/mydesigndoc/_list/mylist/myview include_docs="true" %}

Query parameter values must be valid [JSON](http://www.json.org/). Use the
``jsonify`` filter on any keyword arguments that need to be converted to JSON
before being passed to the database:

    {% couchdb /mydb/_design/mydesigndoc/_list/mylist/myview key=string_with_spaces|jsonify %}