import random
from functools import lru_cache
from urllib.request import urlopen

from skybeard.beards import BeardChatHandler
from skybeard.decorators import onerror


class JitsiMeetBeard(BeardChatHandler):

    __userhelp__ = "Makes jitsi meet room per telegram chat."

    __commands__ = [
        ("videoroom", 'jitsi_meet', 'Sends link for video chat')
    ]

    # __init__ is implicit

    @lru_cache()
    def _get_words(self):
        # Open list of words from:
        # https://github.com/first20hours/google-10000-english
        words_file = urlopen("https://raw.githubusercontent.com/first20hours"
                             "/google-10000-english/master/google-10000-"
                             "english-usa-no-swears-medium.txt")
        words = words_file.read().decode('utf-8').split("\n")
        words.remove('')

        words = [x.capitalize() for x in words]
        return words

    @onerror
    async def jitsi_meet(self, msg):
        chat_id = msg['chat']['id']
        random.seed(chat_id)

        room_name = "".join(
            (random.choice(self._get_words()) for x in range(5)))
        link = "https://meet.jit.si/"+room_name

        await self.sender.sendMessage(
            "Video room (click to join): {l}\n\nJitsi room name: \n\n*{r}*\n\n(On mobile, you may need to install the app)".format(r=room_name, l=link),
            parse_mode='Markdown')
