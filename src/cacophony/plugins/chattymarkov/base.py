"""Chattymarkov plugin base classes."""
import chattymarkov

class ChattyBot:
    """Describe a chattybot bound to some specific discord server."""

    def __init__(self, brain, discord_user, chattyness=0.1, mute=False):
        self._brain = brain
        self._chattyness = chattyness
        self._mute = mute
        self._discord_user = discord_user

    def answer(self, message) -> str:
        """Return an answer after having received `message`.

        If the bot won't answer, then an empty string will be returned. The bot
        will answer if the following conditions are met:
            * The bot must not be mute.
            * A random number between 0 and 1 falls under `self._chattyness`.
            * The bot is mentioned (100% answer rate).

        Args:
            message: The discord message to learn from.

        Returns:
            The message to answer, empty string otherwise.

        """
        if mute:
            return ''  # Bot is mute, nothing to answer

        self._brain.learn(message)

        is_mentioned = self.discord_user in message.mentions
        will_answer = is_mentioned or random.random() < self._chattyness
        
        if will_answer:
            answer = self._brain.generate()  # Pick-up a random sentence.
            if is_mentioned:
                answer = f'<@{message.author.id}> {answer}'
            return answer
        else:
            return ''
