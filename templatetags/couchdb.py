"""
CouchDB template tag based on Django's built-in "url" template tag.
"""
from django import template
from django.conf import settings
from django.template import Node, TemplateSyntaxError
from django.utils import simplejson
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
import re
import urllib


register = template.Library()
# Regex for token keyword arguments
kwarg_re = re.compile(r"(?:(\w+)=)?(.+)")


@register.filter
def jsonify(o):
    """
    Based on Django snippet 1250:
    http://djangosnippets.org/snippets/1250/
    """
    return mark_safe(simplejson.dumps(o))


def get_content(url, **kwargs):
    if hasattr(settings, "COUCHDB_SERVER"):
        server = settings.COUCHDB_SERVER
    else:
        server = "http://localhost:5984"

    url = urllib.basejoin(server, url)
    data = None
    if kwargs:
        # Handle the special case of bulk document retrieval using an array of
        # keys that need to be POSTed.
        if "keys" in kwargs:
            data = simplejson.dumps(
                {"keys": kwargs.pop("keys")}
            )

        url = "%s?%s" % (url, urllib.urlencode(kwargs))

    return urllib.urlopen(url, data).read().strip()


class CouchDbNode(Node):
    def __init__(self, url, kwargs, asvar):
        self.url = url
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        content = get_content(self.url, **kwargs)
        if self.asvar:
            context[self.asvar] = content
            return ''
        else:
            return content


def couchdb(parser, token):
    """
    Returns the content associated with a CouchDB URL and optional parameters.

    For example, use the following code to embed the content of a CouchDB list
    with an include_docs parameter::

        {% couchdb /mydb/_design/mydesigndoc/_list/mylist/myview include_docs="true" %}

    These arguments will be used to get content from the following URL::

        http://localhost:5984/mydb/_design/mydesigndoc/_list/mylist/myview?include_docs=true

    The first argument is a CouchDB url relative to the server defined as
    ``COUCHDB_SERVER`` in settings.py. Keyword arguments are space-separated
    values that will be used to build a query string for the URL.
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (url relative to CouchDB server)" % bits[0])
    url = bits[1]
    kwargs = {}
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    # Now all the bits are parsed into new format,
    # process them as template vars
    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to couchdb tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)

    return CouchDbNode(url, kwargs, asvar)
couchdb = register.tag(couchdb)
