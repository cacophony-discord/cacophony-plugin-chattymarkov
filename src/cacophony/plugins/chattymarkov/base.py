"""Chattymarkov plugin base classes."""
import chattymarkov

class ChattyBot:
    """Describe a chattybot bound to some specific discord server."""

    def __init__(self, brain, chattyness=0.1):
        self._chattyness = chattyness
