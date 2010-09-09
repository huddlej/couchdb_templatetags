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

Specify optional query parameters exactly as you do in the browser. For example,
the following example includes the output of a CouchDB list with documents
included:

    {% couchdb /mydb/_design/mydesigndoc/_list/mylist/myview?include_docs=true %}

You can specify dynamic values for query parameters by using [named
placeholders](http://docs.python.org/library/stdtypes.html#string-formatting-operations)
exactly as you would with any Python string and passing keyword arguments:

    {% couchdb /mydb/_design/mydesigndoc/_list/mylist/myview?limit=%(limit)s limit=request.GET.limit %}

Named placeholders come in handy when you need to build more complex queries
such as [view collations](http://wiki.apache.org/couchdb/View_collation) with
start and end keys:

    {% couchdb /mydb/_design/mydesigndoc/_list/mylist/myview?startkey=["%(key)s","A"]&endkey=["%(key)s","Z"] key=mykey %}

Query parameter values must be valid [JSON](http://www.json.org/). Use the
``jsonify`` filter on any keyword arguments that need to be converted to JSON
before being passed to the database:

    {% couchdb /mydb/_design/mydesigndoc/_list/mylist/myview?key=%(key)s key=string_with_spaces|jsonify %}
