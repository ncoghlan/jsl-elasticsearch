"""High level JSL rendering tests"""
import jsl
from jsl_elasticsearch import TextField, render_es_template

import unittest

class TestRendering(unittest.TestCase):

    def _check_rendering(self, document, title, role, expected):
        rendered = render_es_template(document, title, role)
        self.assertEqual(rendered, expected)

    def test_primitive_fields(self):
        self._check_rendering(PrimitiveFields,
                              "project-primitive_fields",
                              "v1-0-0",
                              expected_primitive_template)

    def test_nested_documents(self):
        self._check_rendering(NestedDocuments,
                              "project-nested_documents",
                              "v1-0-0",
                              expected_nested_template)

    def test_versioned_documents(self):
        title = "project-multiversion_document"
        self._check_rendering(MultiversionDocument,
                              "project-multiversion_document",
                              "v1-0-0",
                              expected_multiversion_v1_0_0_template)
        self._check_rendering(MultiversionDocument,
                              "project-multiversion_document",
                              "v2-0-0",
                              expected_multiversion_v2_0_0_template)

#####################################################
# Example input documents for rendering tests
#####################################################

# Support required primitive fields
class PrimitiveFields(jsl.document.Document):
    single_str = jsl.StringField()
    str_array = jsl.ArrayField(jsl.StringField())
    text_data = TextField()
    text_array = jsl.ArrayField(TextField())
    single_int = jsl.IntField()
    int_array = jsl.ArrayField(jsl.IntField())
    single_float = jsl.NumberField()
    float_array = jsl.ArrayField(jsl.NumberField())

# Support nested documents
class NestedDocuments(jsl.document.Document):
    single_doc = jsl.DocumentField(PrimitiveFields, as_ref=True)
    doc_array = jsl.ArrayField(jsl.DocumentField(PrimitiveFields, as_ref=True))
    single_dict = jsl.DictField(dict(str_key=jsl.StringField(), int_key=jsl.IntField()))
    dict_array = jsl.ArrayField(jsl.DictField(dict(str_key=jsl.StringField(), int_key=jsl.IntField())))

# Support generating version specific mappings
ROLE_v1_0_0 = "v1-0-0"
ROLE_v2_0_0 = "v2-0-0"

ROLE_TITLE = jsl.roles.Var({
    ROLE_v1_0_0: "MultiversionDocument v1-0-0",
    ROLE_v2_0_0: "MultiversionDocument v2-0-0",
})

class MultiversionDocument(jsl.document.Document):
    class Options(object):
        title = ROLE_TITLE

    with jsl.roles.Scope(ROLE_v1_0_0) as v1:
        v1.subfield = jsl.fields.NumberField()
    with jsl.roles.Scope(ROLE_v2_0_0) as v2:
        v2.subfield = jsl.fields.IntField()

#####################################################
# Expected results from rendering example documents
#####################################################
expected_primitive_template = {
    "template": "project-primitive_fields-template_v1_0_0-*",
    "settings": {},
    "aliases": {
        "project-primitive_fields": {}
    },
    "mappings": {
        "content": {
            "properties": {
                "@timestamp": {
                    "type": "date",
                    "format": "dateOptionalTime"
                },
                "single_str": {
                    "index": "not_analyzed",
                    "type": "string",
                },
                "str_array": {
                    "index": "not_analyzed",
                    "type": "string",
                },
                "text_data": {
                    "type": "string"
                },
                "text_array": {
                    "type": "string"
                },
                "single_float": {
                    "type": "float"
                },
                "float_array": {
                    "type": "float"
                },
                "single_int": {
                    "type": "integer"
                },
                "int_array": {
                    "type": "integer"
                },
            }
        }
    }
}

expected_nested_template = {
  "template": "project-nested_documents-template_v1_0_0-*",
  "settings": {},
  "aliases": {
    "project-nested_documents": {}
  },
  "mappings": {
    "content": {
      "properties": {
        "@timestamp": {
          "type": "date",
          "format": "dateOptionalTime"
        },
        "single_doc": {
          "type": "nested",
          "properties": {
            "single_str": {
              "type": "string",
              "index": "not_analyzed",
            },
            "str_array": {
              "type": "string",
              "index": "not_analyzed",
            },
            "text_data": {
              "type": "string"
            },
            "text_array": {
              "type": "string"
            },
            "single_int": {
              "type": "integer"
            },
            "int_array": {
              "type": "integer"
            },
            "single_float": {
              "type": "float"
            },
            "float_array": {
              "type": "float"
            }
          }
        },
        "doc_array": {
          "type": "nested",
          "properties": {
            "single_str": {
              "type": "string",
              "index": "not_analyzed",
            },
            "str_array": {
              "type": "string",
              "index": "not_analyzed",
            },
            "text_data": {
              "type": "string"
            },
            "text_array": {
              "type": "string"
            },
            "single_int": {
              "type": "integer"
            },
            "int_array": {
              "type": "integer"
            },
            "single_float": {
              "type": "float"
            },
            "float_array": {
              "type": "float"
            }
          }
        },
        "single_dict": {
          "type": "nested",
          "properties": {
            "int_key": {
              "type": "integer"
            },
            "str_key": {
              "type": "string",
              "index": "not_analyzed",
            }
          }
        },
        "dict_array": {
          "type": "nested",
          "properties": {
            "int_key": {
              "type": "integer"
            },
            "str_key": {
              "type": "string",
              "index": "not_analyzed",
            }
          }
        }
      }
    }
  }
}


expected_multiversion_v1_0_0_template = {
  "template": "project-multiversion_document-template_v1_0_0-*",
  "settings": {},
  "aliases": {
    "project-multiversion_document": {}
  },
  "mappings": {
    "content": {
      "properties": {
        "@timestamp": {
          "type": "date",
          "format": "dateOptionalTime"
        },
        "subfield": {
          "type": "float"
        }
      }
    }
  }
}

expected_multiversion_v2_0_0_template = {
  "template": "project-multiversion_document-template_v2_0_0-*",
  "settings": {},
  "aliases": {
    "project-multiversion_document": {}
  },
  "mappings": {
    "content": {
      "properties": {
        "@timestamp": {
          "type": "date",
          "format": "dateOptionalTime"
        },
        "subfield": {
          "type": "integer"
        }
      }
    }
  }
}

