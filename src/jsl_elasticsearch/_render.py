from collections import OrderedDict
from functools import singledispatch

import jsl
from ._fields import TextField

def render_es_template(document, title, role, doc_type="content"):
    """Render an ElasticSearch time series template for given JSL document

    Template name is generated from the given *title* and *role*
    Document variables are resolved using the given *role*
    *doc_type* specifies the ElasticSearch mapping name (default: "content")
    """
    template = "{}-template_{}-*".format(title, role.replace("-", "_"))
    settings = {}
    aliases = {
        title: {}
    }
    doc_properties = render_es_mapping(document, role, add_timestamp=True)
    mappings = {
        doc_type: {
            "properties": doc_properties
        }
    }
    return OrderedDict((
        ("template", template),
        ("settings", settings),
        ("aliases", aliases),
        ("mappings", mappings),
    ))

def render_es_mapping(document, role, *, add_timestamp=False):
    """Render an ElasticSearch document mapping for given JSL document

    Document variables are resolved using the given *role*.
    Setting *add_timestamp* will add a ``dateOptionalTime`` formatted
    ``"@timestamp"`` field
    """
    result = OrderedDict()
    if add_timestamp:
        result["@timestamp"] = OrderedDict((
            ("type", "date"),
            ("format", "dateOptionalTime"),
        ))
    for name, field in document.resolve_and_iter_fields(role):
        result[name] = render_es_property(field, role)
    return result

@singledispatch
def render_es_property(jsl_field, role):
    """Render an individual JSL field as an ElasticSearch property"""
    raise NotImplementedError("Unknown JSL Field type: {!r}".format(type(jsl_field)))

@render_es_property.register(jsl.DocumentField)
def _render_document_field(jsl_field, role):
    return OrderedDict((
        ("type", "nested"),
        ("properties", render_es_mapping(jsl_field.document_cls, role)),
    ))

@render_es_property.register(jsl.DictField)
def _render_dict_field(jsl_field, role):
    properties, properties_role = jsl_field.resolve_attr('properties', role)
    result = OrderedDict()
    for name, field in sorted(properties.items()):
        result[name] = render_es_property(field, role)
    return OrderedDict((
        ("type", "nested"),
        ("properties", result),
    ))

@render_es_property.register(jsl.ArrayField)
def _render_array_field(jsl_field, role):
    # All ElasticSearch fields are implicitly arrays
    # so just render the contained field type
    return render_es_property(jsl_field.items, role)

@render_es_property.register(jsl.StringField)
def _render_string_field(jsl_field, role):
    # Note: marking the field as "not_analyzed" also implicitly switches
    # the default value of "doc_types" to True, enabling efficient lookups
    # based on the whole field value (rather than the field contents, which
    # is the default for analyzed strings)
    return OrderedDict((
        ("type", "string"),
        ("index", "not_analyzed"),
    ))

@render_es_property.register(TextField)
def _render_text_field(jsl_field, role):
    return {
        "type": "string",
    }

@render_es_property.register(jsl.IntField)
def _render_int_field(jsl_field, role):
    return {
        "type": "integer",
    }

@render_es_property.register(jsl.NumberField)
def _render_int_field(jsl_field, role):
    return {
        "type": "float",
    }
