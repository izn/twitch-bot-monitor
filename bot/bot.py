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

server = 'irc.chat.twitch.tv'
nick = os.environ.get('TWITCH_LOGIN')
passwd = os.environ.get('TWITCH_OAUTH')
channel = os.environ.get('TWITCH_CHANNEL')
port = 6667

s = socket.socket()
s.connect((server, port))
s.send(bytes('PASS %s\r\n' % passwd, 'utf-8'))
s.send(bytes('NICK %s\r\n' % nick, 'utf-8'))
s.send(bytes('JOIN #%s\r\n' % channel.lower(), 'utf-8'))

while 1:
    buffered = s.recv(1024)
    data = buffered.decode('utf-8')

    # irc-protocol expressions
    ping = re.search(r'^PING', data)
    privmsg = re.search(r'^:(\w+)!(?:\w+)@(?:[\w\.]+)\sPRIVMSG\s#(\w+)\s:(.+?)\r\n$', data)

    if ping is not None:
        print("[PING] Sending PONG :)")
        s.send(b'PONG :tmi.twitch.tv\r\n')

    if privmsg is not None:
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
