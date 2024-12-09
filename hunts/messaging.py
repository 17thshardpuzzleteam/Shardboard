import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DiscordInterface:
    URL = os.getenv('DISCORD_WEBHOOK_URL')
    USERNAME = 'Shardboard'

    def send_message(self, content):
        if len(content) >= 2000:
            content = content[:1996] + '...'
        requests.post(self.URL, data={'username': self.USERNAME, 'content': content})


discord_interface = DiscordInterface()
