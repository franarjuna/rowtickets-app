from __future__ import absolute_import, unicode_literals

from rowticket.settings.base import *

DEBUG = False

try:
    from .local import * # pylint: disable=wildcard-import
except ImportError:
    pass
