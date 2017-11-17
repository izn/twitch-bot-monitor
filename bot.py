import socket
import string
import re
import redis
import sys


r = redis.Redis()

server = 'irc.chat.twitch.tv'
passwd = ''
nick = ''
channel = sys.argv[0]
port = 6667

s = socket.socket()
s.connect((server, port))
s.send(bytes("PASS %s\r\n" % passwd, "UTF-8"))
s.send(bytes("NICK %s\r\n" % nick, "UTF-8"))
s.send(bytes("JOIN %s\r\n" % channel, "UTF-8"))

while 1:
    buffered = s.recv(1024)
    data = buffered.decode('utf-8')

    # IRC Protocol
    ping = re.search('^PING', data)
    privmsg = re.search('^:(\w+)!(?:\w+)@(?:[\w\.]+)\sPRIVMSG\s#(\w+)\s:(.+?)\\r\\n$', data)

    if ping is not None:
        print("[PING] Sending PONG :)")
        s.send(b'PONG :tmi.twitch.tv\r\n')

    if privmsg is not None:
        _user = privmsg.group(1).lower()
        _channel = privmsg.group(2).lower()
        _msg = privmsg.group(3).lower()

        print('#{0} @ {1}: {2}'.format(_channel, _user, _msg))

        for msg in list(set(_msg.split(" "))):
            if len(msg) > 2:
                filtered_word = msg.strip(string.punctuation)
                r.zincrby(_channel, filtered_word, 1)
