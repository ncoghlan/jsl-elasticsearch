# Project metadata
__version__ = "0.1.dev0"

__title__ = "jsl_elasticsearch"
__description__ = "Generate ElasticSearch templates from JSL"
__uri__ = "https://github.com/ncoghlan/jsl_elasticsearch"
__doc__ = __description__ + " <" + __uri__ + ">"

__author__ = "Nick Coghlan"
__email__ = "ncoghlan@gmail.com"

__license__ = "MIT"
__copyright__ = "Copyright (c) 2016 Nick Coghlan"

# Public API
__all__ = [
    "TextField",
    "render_es_template",
    "render_es_mapping",
    "render_es_property",
]

from ._fields import (
    TextField,
)
from ._render import (
    render_es_template,
    render_es_mapping,
    render_es_property
)
