from twisted.words.protocols import irc

from . import config
from .plugin import PluginManager


class CommandsAccessor(object):
    def do_nothing(self, *args, **kwargs):
        pass
    @classmethod
    def create(cls, **kwargs):
        accessor = cls()
        for method_name in ('topic', 'mode', 'msg', 'notice',
                            'whois', 'ping'):
            setattr(accessor, method_name,
                    kwargs.get(method_name, cls.do_nothing))
        return accessor


class Yabbit(irc.IRCClient):

    def __init__(self, factory):
        self.plugin_manager = PluginManager()
        self.config = config
        self.factory = factory
        self.accessor = CommandsAccessor(
            msg=self.msg, topic=self.topic, mode=self.mode, notice=self.notice,
            whois=self.whois, ping=self.ping,
        )

    @property
    def nickname(self):
        """
        Returns bot's nickname
        """
        return config.NETWORKS[self.factory.network]['nickname']

    @property
    def channels(self):
        """
        Returns list of channels
        """
        return config.NETWORKS[self.factory.network]['channels']

    def signedOn(self):
        """
        Actions which will be executed after connecting to a server
        """
        for channel in self.factory.channels:
            self.join(channel)

    def privmsg(self, user, channel, msg):
        """
        Runs plugins when command defined in plugin class has been sent
        (directly or on a channel)
        """
        PluginManager.dispatch('privmsg', user, channel, msg)

    def noticed(self, user, channel, message):
        PluginManager.dispatch('noticed', user, channel, message)

    def topicUpdated(self, user, channel, newTopic):
        PluginManager.dispatch('topic_updated', user, channel, newTopic)

    def userJoined(self, user, channel):
        PluginManager.dispatch('user_joined', user, channel)

    def userLeft(self, user, channel):
        PluginManager.dispatch('user_left', user, channel)

    def userKicked(self, kickee, channel, kicker, message):
        PluginManager.dispatch('user_left', kickee, channel, kicker, message)

    def action(self, user, channel, data):
        PluginManager.dispatch('action', user, channel, data)
