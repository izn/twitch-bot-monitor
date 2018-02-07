import dotenv
import nltk.corpus
import os
import re
import redis
import socket
import string
import unicodedata

nltk.download('stopwords')
dotenv.load_dotenv(dotenv.find_dotenv())

r = redis.Redis()


def parse_pingpong(data):
    return re.search(r'^PING', data)


def parse_privmsg(data):
    return re.search(r'^:(\w+)!(?:\w+)@(?:[\w\.]+)\sPRIVMSG\s#(\w+)\s:(.+)\r\n$', data)


class Bot(object):
    def __init__(self):
        self.server = 'irc.chat.twitch.tv'
        self.nick = os.environ.get('TWITCH_LOGIN')
        self.passwd = os.environ.get('TWITCH_OAUTH')
        self.channel = os.environ.get('TWITCH_CHANNEL')
        self.port = 6667

    def send(self, data):
        raw = '{}\r\n'.format(data)
        self.s.send(raw.encode())

    def start(self):
        self.s = socket.socket()
        self.s.connect((self.server, self.port))

        self.send('PASS {}'.format(self.passwd))
        self.send('NICK {}'.format(self.nick))
        self.send('JOIN #{}'.format(self.channel.lower()))

        while True:
            buffered = self.s.recv(1024)
            data = buffered.decode()

            privmsg = parse_privmsg(data)

            if parse_pingpong(data):
                print("[PING] Sending PONG :)")
                self.send('PONG :tmi.twitch.tv')

            if privmsg:
                user = privmsg.group(1).lower()
                channel = privmsg.group(2).lower()
                msg = privmsg.group(3).lower()

                print('#{0} @ {1}: {2}'.format(channel, user, msg))

                words = [w.strip(string.punctuation) for w in msg.split(" ")]
                words = [w for w in words if w not in nltk.corpus.stopwords.words('portuguese')]

                for word in set(words):
                    filtered_word = unicodedata.normalize('NFD', word)

                    if len(filtered_word) > 2:
                        r.zincrby(channel, filtered_word)


if __name__ == '__main__':
    bot = Bot()
    bot.start()
