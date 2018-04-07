"""Cacophony plugin for chattymarkov: generate random sentences."""
from collections import defaultdict
import logging

from cacophony.base import Plugin

from .__about__ import (__author__, __copyright__, __email__, __license__,
                        __summary__, __title__, __uri__, __version__)

from .hooks import learn

logger = logging.getLogger(__name__)

__all__ = [
    '__author__',
    '__copyright__',
    '__email__',
    '__license__',
    '__summary__',
    '__title__',
    '__uri__',
    '__version__',
    'hooks',
]

hooks = {
    'on_message': [learn]
}


class ChattymarkovPlugin(Plugin):
    """Chattymarkov plugin for cacophony."""
    def __init__(self, *args, **kwargs):
        """Instantiate chattymarkov plugin."""
        super().__init__(*args, **kwargs)
        self.chattybots = {}

    async def on_ready(self):
        """Instantiate "brains" per server once the bot is ready."""
        for server in self.bot.servers:
            logger.info("Instanciate brain for server %s", server)
            self.chattybots[server.id] = {}


plugin_class = ChattymarkovPlugin
