__author__ = 'roosevelt'

import os
import sys

def is_frozen():
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if is_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))

