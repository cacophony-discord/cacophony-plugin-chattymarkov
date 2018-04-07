"""Chattymarkov hooks."""
import logging

import chattymarkov

logger = logging.getLogger(__name__)

async def learn(app, message):
    """Learn from the content of `message` and generate an answer eventually.

    Depending on the bot settings, an answer might be generated or not. The
    following conditions must be met for the bot to answer:
        - The bot must not be mute.
        - The bot is mentionned (100% answer rate).
        - A random number between 0 and 1 falls below the chattyness rate.

    Args:
        message: The discord message to learn from.

    """
    # Get the server id or skip everything.
    try:
        server_id = message.server.id
    except AttributeError:
        logger.warning("Could not get the server id from the message.")
    else:
        pass        
