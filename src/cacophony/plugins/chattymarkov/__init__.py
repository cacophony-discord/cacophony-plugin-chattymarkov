"""Cacophony plugin for chattymarkov: generate random sentences into the chat."""

from .__about__ import (__author__, __copyright__, __email__, __license__,
                        __summary__, __title__, __uri__, __version__)

from .hooks import learn

__all__ = [
    '__author__',
    '__copyright__',
    '__email__',
    '__license__',
    '__summary__',
    '__title__',
    '__uri__',
    '__version__',
]

hooks = {
    'on_message': [learn]
}
