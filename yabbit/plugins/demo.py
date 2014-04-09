

class Plugin(object):
    """
    Usage: .ping - returns 'pong' message
    """
    command = 'ping'

    def run(self, bot, nickname, hostmask, channel, msg):
        bot.msg(channel, '{}: pong!'.format(nickname))