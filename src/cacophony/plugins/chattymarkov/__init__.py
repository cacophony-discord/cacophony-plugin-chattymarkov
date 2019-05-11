"""Cacophony plugin for chattymarkov: generate random sentences."""
from collections import defaultdict
import os
import logging

import chattymarkov
from cacophony.base import Hook, Plugin

from .__about__ import (__author__, __copyright__, __email__, __license__,
                        __summary__, __title__, __uri__, __version__)

from .base import ChattyBot
from .hooks import create_new_brain, learn

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
    Hook.ON_MESSAGE: [learn],
    Hook.ON_SERVER_JOIN: [create_new_brain]
}


class ChattymarkovPlugin(Plugin):
    """Chattymarkov plugin for cacophony."""

    def __init__(self, *args, **kwargs):
        """Instantiate chattymarkov plugin."""
        super().__init__(*args, **kwargs)
        self._brain_string = os.environ.get("CHATTYMARKOV_BRAIN_STRING",
                                            "memory://")
        self.chattybots = defaultdict(ChattyBot)

    def build_chattybot(self, server_id, chattyness=0.1):
        """Build a chattybot for server identified by `server_id`.

        Args:
            server_id: The server id to assign the new chattybot to.
            chattyness: The chattyness rate for the newly created bot.

        Returns:
            An instance of `ChattyBot`.

        """
        return ChattyBot(brain=chattymarkov.ChattyMarkovAsync(
            connect_string=self._brain_string, prefix=server_id),
            discord_user=self.bot.discord_client.user,
            chattyness=chattyness)

    async def on_ready(self):
        """Instantiate "brains" per server once the bot is ready."""
        for server in self.bot.guilds:
            self._bot.info("Instanciate brain for server %s", server)
            chattyness = float(self.bot.get_config(server.id,
                                                   "chattymarkov.chattyness",
                                                   0.1))
            self.chattybots[server.id] = self.build_chattybot(server.id,
                                                              chattyness)
            await self.chattybots[server.id].connect()
            self._bot.info("Servers are: %s", self.chattybots.keys())


plugin_class = ChattymarkovPlugin
