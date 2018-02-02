from twitchbot.bot import parse_privmsg, parse_pingpong


class TestBotParsing(object):
    def test_privmsg(self):
        test_str = ':user!user@user.twitch.tv PRIVMSG #channel :test msg\r\n'

        result = parse_privmsg(test_str)

        assert result is not None

    def test_pingpong(self):
        test_str = 'PING tmi.twitch.tv\r\n'
        result = parse_pingpong(test_str)

        assert result is not None
