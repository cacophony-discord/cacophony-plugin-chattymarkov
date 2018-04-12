"""Chattymarkov hooks."""
import logging

import chattymarkov

logger = logging.getLogger(__name__)


async def _chattybot_learn(app, chattybot, message):
    """Private. Let `chattybot` learn `message` and answer through `app`.
    
    Args:
        app: The application instance.
        chattybot: The chattybot instance responsible for generating the
            answer.
        message: The discord message that has been received.
    
    """
    answer = chattybot.answer(message)
    if answer:
        await app.send_message(message.channel, answer)


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
    logger.warning("Todo: learn from '%s'", message.content)
    try:
        server_id = message.server.id
    except AttributeError:
        logger.warning("Could not get the server id from the message.")
    else:
        # XXX: Isn't it an ugly way to get the right chattybot?
        try:
            chattybot = app.plugins['chattymarkov'].chattybots[server_id]
        except KeyError:
            logger.warning("No chattybot found for server %s. Skipping...",
                           server_id)
        else:
            await _chattybot_learn(app, chattybot, message)
