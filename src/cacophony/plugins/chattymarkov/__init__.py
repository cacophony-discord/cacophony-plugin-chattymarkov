"""Cacophony plugin for chattymarkov: generate random sentences."""
from collections import defaultdict
import os
import logging

import chattymarkov
from cacophony.base import Hook, Plugin

from .__about__ import (__author__, __copyright__, __email__, __license__,
                        __summary__, __title__, __uri__, __version__)

from .base import ChattyBot
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
    'plugin_class',
]

hooks = {
    Hook.ON_MESSAGE: [learn]
}


class ChattymarkovPlugin(Plugin):
    """Chattymarkov plugin for cacophony."""
    def __init__(self, *args, **kwargs):
        """Instantiate chattymarkov plugin."""
        super().__init__(*args, **kwargs)
        self._brain_string = os.environ.get("CHATTYMARKOV_BRAIN_STRING",
                                            "memory://")
        self.chattybots = defaultdict(ChattyBot)

    async def on_ready(self):
        """Instantiate "brains" per server once the bot is ready."""
        for server in self.bot.servers:
            logger.info("Instanciate brain for server %s", server)
            chattyness = float(self.bot.get_config(server.id,
                                                   "chattymarkov.chattyness",
                                                   0.1))
            self.chattybots[server.id] = ChattyBot(
                brain=chattymarkov.ChattyMarkov(
                    connect_string=self._brain_string,
                    prefix=server.id),
                discord_user=self.bot.discord_client.user,
                chattyness=chattyness)


plugin_class = ChattymarkovPlugin
