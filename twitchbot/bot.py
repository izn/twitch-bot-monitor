import dotenv
import nltk.corpus
import socket
import string
import os
import re
import redis
import unicodedata

nltk.download('stopwords')
dotenv.load_dotenv(dotenv.find_dotenv())

r = redis.Redis()

SERVER = 'irc.chat.twitch.tv'
NICK = os.environ.get('TWITCH_LOGIN')
PASSWD = os.environ.get('TWITCH_OAUTH')
CHANNEL = os.environ.get('TWITCH_CHANNEL')
PORT = 6667


def parse_pingpong(data):
    return re.search(r'^PING', data)


def parse_privmsg(data):
    return re.search(r'^:(\w+)!(?:\w+)@(?:[\w\.]+)\sPRIVMSG\s#(\w+)\s:(.+)\r\n$', data)


class Bot(object):
    def __init__(self):
        self.s = socket.socket()
        self.s.connect((SERVER, PORT))

        self.s.send(bytes('PASS %s\r\n' % PASSWD, 'utf-8'))
        self.s.send(bytes('NICK %s\r\n' % NICK, 'utf-8'))
        self.s.send(bytes('JOIN #%s\r\n' % CHANNEL.lower(), 'utf-8'))

    def start(self):
        while True:
            buffered = self.s.recv(1024)
            data = buffered.decode('utf-8')

            privmsg = parse_privmsg(data)

            if parse_pingpong(data):
                print("[PING] Sending PONG :)")
                self.s.send(b'PONG :tmi.twitch.tv\r\n')

            if privmsg:
                _user = privmsg.group(1).lower()
                _channel = privmsg.group(2).lower()
                _msg = privmsg.group(3).lower()

                print('#{0} @ {1}: {2}'.format(_channel, _user, _msg))

                words = [w.strip(string.punctuation) for w in _msg.split(" ")]
                words = [w for w in words if w not in nltk.corpus.stopwords.words('portuguese')]

                for word in set(words):
                    filtered_word = unicodedata.normalize('NFD', word)

                    if len(filtered_word) > 2:
                        r.zincrby(_channel, filtered_word, 1)


if __name__ == '__main__':
    bot = Bot()
    bot.start()
