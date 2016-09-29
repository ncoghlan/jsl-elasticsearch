JSL -> ElasticSearch
====================

``jsl_elasticsearch`` generates ElasticSearch mappings from JSL definitions.

It requires Python 3.4 or later (mainly for ``functools.singledispatch``).

It is specifically aimed at use cases where ElasticSearch is being used as a
time series database for JSON data with schemas defined using the
`jsl <http://jsl.readthedocs.io>`__ Python library.

The main API is ``jsl_elasticsearch.render_es_template``::

   def render_es_template(document, title, role, doc_type="content"):
       """Render an ElasticSearch time series template for given JSL document

       Template name is generated from the given *title* and *role*
       Document variables are resolved using the given *role*
       *doc_type* specifies the ElasticSearch mapping name (default: "content")
       """

The ``@timestamp`` field expected by Kibana is added automatically, and
string fields are flagged as ``not_analyzed`` by default (so ElasticSearch
treats them as opaque tokens, rather than as plain text fields to be
analyzed for full text search)

The following JSL field types are currently supported:

* ``jsl.StringField``
* ``jsl.NumberField``
* ``jsl.IntField``
* ``jsl.ArrayField``
* ``jsl.DictField``
* ``jsl.DocumentField``

An additional field type is also defined:

* ``jsl_elasticsearch.TextField``

With string fields being flagged as opaque tokens by default, ``TextField``
is a new ``StringField`` subclass that flags the field for full text search
in the ElasticSearch mapping, but is otherwise handled exactly like
``StringField`` by JSL.
