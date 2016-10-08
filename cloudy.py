from wordcloud  import WordCloud, ImageColorGenerator
from twitchChat import TwitchChat
from time       import sleep
from PIL        import Image
import numpy as np
from ShiftText import ShiftText

class Cloudy():
    host = 'irc.twitch.tv'
    port = 6667

    def __init__(self, options):
        self.nick         = options.get('nickname', '')
        self.password     = options.get('oauth', '')
        self.channel      = options.get('channel', '')
        self.limit        = options.get('limit', 1500)
        self.image        = options.get('image', '')
        
        self.mask         = None
        self.image_colors = None

        if self.image:
            try:
                self.image = Image.open(self.image)
                self.mask  = np.array(self.image)
            except:
                print("No image!")
            self.image_colors = ImageColorGenerator(self.mask)

        self.chat = TwitchChat(Cloudy.host, Cloudy.port, self.nick, self.password)
        self.chat.joinChannel(self.channel)

        self.buffer = ShiftText(self.limit)

    def generateImage(self):
        messages = self.chat.fetchMessages()
        if len(messages) > 0:
            for username, message, unfilteredMessage in messages:
                self.buffer.push(message)

            if len(self.buffer) > 10:
                if self.mask != None:
                    width = self.mask.shape[1]
                    height = self.mask.shape[0]
                    scale = 640 / width
                    wordcloud = WordCloud(max_words=5000, scale=scale, mask=self.mask, color_func=self.image_colors).generate(self.buffer.buffer)
                else:
                    wordcloud = WordCloud(max_words=5000, scale=2).generate(self.buffer.buffer)

                image = wordcloud.to_image()
                return image

    def onChatMessage(self, username, message, unfilteredMessage):
        self.buffer.push(message)

if __name__ == "__main__":
    clouds = Cloudy({
        'nickname': 'combinatorilliance',
        'oauth': 'oauth:6f7hbzb6wlznzkrb0vdsqntutj2h7f',
        'channel': '#drfeelgood',
        'limit': 1500,
        'image': 'qtpie.jpg'
    })

