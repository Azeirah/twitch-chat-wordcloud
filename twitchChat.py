import socket
import re
from queue import Queue
import threading
import time

class TwitchChat():
    def __init__(self, host, port, nick, password):
        """TwitchChat handles reading from any twitch chat channel. It utilizes threading
        to continuously receive messages from a given channel.
        All messages will be stored in a queue, 
        use .fetchMessages() to receive and empty the underlying queue of messages

        >>> chat = TwitchChat(...)
        >>> chat.joinChannel('#imaqtpie')
        >>> time.sleep(5)
        >>> messages = chat.fetchMessages()
        >>> for username, message, unfilteredMessage in messages:
        >>>     print(username, message)
        """
        self.nick = nick
        self.password = password
        self.host = host
        self.port = port
        self.chatBuffer = Queue()
        self.joined = False

        # precompile all regexes for miniscule and honestly not worth-it performance boosts
        self.RE_chat_msg = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        self.RE_username = re.compile(r"\w+")

    def joinChannel(self, channel):
        if not self.joined:
            self.channel = channel
            threading.Thread(target=self.receiveChatMessages).start()
            self.joined = True
        else:
            Exception("TwitchChat only supports one channel right now, create another instance instead")

    def receiveChatMessages(self):
        """Private method, don't use this outside of this class"""
        chatSocket = socket.socket()
        chatSocket.connect((self.host, self.port))
        chatSocket.send("PASS {}\r\n".format(self.password).encode("utf-8"))
        chatSocket.send("NICK {}\r\n".format(self.nick).encode("utf-8"))
        chatSocket.send("JOIN {}\r\n".format(self.channel).encode("utf-8"))

        while True:
            response = chatSocket.recv(4096).decode('utf-8', errors='ignore')
            # respond to pings with pongs :D
            if response == "PING :tmi.twitch.tv\r\n":
                chatSocket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            else:
                if len(response) == 0:
                    continue
                try:
                    username = re.search(self.RE_username, response).group(0)
                except:
                    print("regex error! response = '" + response + "'. Len =", len(response))
                message = self.RE_chat_msg.sub("", response).rstrip('\n')
                if username == self.nick:
                    continue
                if 'tmi' in message:
                    continue

                self.chatBuffer.put((username, message, response))
            time.sleep(0.01)

    def fetchMessages(self):
        """Empty and retrieve the contents of the underlying chat queue"""
        messages = []
        while not self.chatBuffer.empty():
            messages.append(self.chatBuffer.get())
        return messages
