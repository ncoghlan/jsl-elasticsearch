"""Additional fields needed to disambiguate desired ElasticSearch output"""
import jsl

class TextField(jsl.StringField):
    """String field that gets analysed as text in ElasticSearch

    By default, JSL string fields are marked as opaque tokens by the mapping
    generator. Using this subclass instead of a normal jsl.StringField changes
    the ElasticSearch mapping generated to an analysed field without altering
    the normal JSL jsonschema output.
    """
