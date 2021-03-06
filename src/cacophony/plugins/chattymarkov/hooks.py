"""Chattymarkov hooks."""
import logging

logger = logging.getLogger(__name__)


async def _chattybot_learn(app, chattybot, message):
    """Private. Let `chattybot` learn `message` and answer through `app`.

    Args:
        app: The application instance.
        chattybot: The chattybot instance responsible for generating the
            answer.
        message: The discord message that has been received.

    """
    answer = await chattybot.answer(message)
    logger.info("Chattymarkov will answer '%s'", answer)
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
        app: The cacophony application.
        message: The discord message to learn from.

    """
    # Get the server id or skip everything.
    try:
        guild_id = str(message.guild.id)
    except AttributeError:
        logger.warning("Could not get the guild id from the message.")
    else:
        # XXX: Isn't it an ugly way to get the right chattybot?
        try:
            chattybot = app.plugins['chattymarkov'].chattybots[guild_id]
        except (KeyError, TypeError) as exn:
            logger.warning("No chattybot found for guild %s: '%s'",
                           guild_id, exn)
        else:
            await _chattybot_learn(app, chattybot, message)
    return message


async def create_new_brain(app, guild):
    """Create a new brain for `guild`, through `app`.

    Basically, this coroutine will instantiate a new chattybot for `server`
    without the need to reboot the bot.

    Args:
        app: The cacophony application.
        server: The server being joined.

    """
    logger.info("Create new brain for guild id '%s'.", guild.id)
    plugin = app.plugins['chattymarkov']
    chattybot = plugin.build_chattybot(guild.id)
    await chattybot.connect()
    app.plugins['chattymarkov'].chattybots[guild.id] = chattybot
