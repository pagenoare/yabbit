from twisted.words.protocols import irc

import config
from plugin import PluginManager


class CommandsAccessor(object):

    def do_nothing(self, *args, **kwargs):
        pass

    @classmethod
    def create(cls, **kwargs):
        accessor = cls()
        for attr_name in ('topic', 'mode', 'msg', 'notice',
                          'whois', 'ping', 'connected_channels'):
            setattr(accessor, attr_name,
                    kwargs.get(attr_name, cls.do_nothing))
        return accessor


class Yabbit(irc.IRCClient):

    def __init__(self, factory):
        self.plugin_manager = PluginManager()
        self.config = config
        self.factory = factory
        self._connected_channels = []
        self.accessor = CommandsAccessor.create(
            msg=self.msg, topic=self.topic, mode=self.mode, notice=self.notice,
            whois=self.whois, ping=self.ping,
            connected_channels=self.connected_channels,
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
        for channel in self.channels:
            self.join(channel)

    def privmsg(self, user, channel, msg):
        """
        Runs plugins when command defined in plugin class has been sent
        (directly or on a channel)
        """
        PluginManager.dispatch(self, 'privmsg', user, channel, msg)

    def noticed(self, user, channel, message):
        PluginManager.dispatch(self, 'noticed', user, channel, message)

    def topicUpdated(self, user, channel, newTopic):
        PluginManager.dispatch(self, 'topic_updated', user, channel, newTopic)

    def userJoined(self, user, channel):
        PluginManager.dispatch(self, 'user_joined', user, channel)

    def userLeft(self, user, channel):
        PluginManager.dispatch(self, 'user_left', user, channel)

    def userKicked(self, kickee, channel, kicker, message):
        PluginManager.dispatch(self, 'user_left', kickee, channel, kicker, message)

    def action(self, user, channel, data):
        PluginManager.dispatch(self, 'action', user, channel, data)

    def joined(self, channel):
        self._connected_channels.append(channel)

    def kickedFrom(self, channel, kicker, message):
        self._connected_channels.remove(channel)

    # TODO: leave unsupported

    @property
    def connected_channels(self):
        return list(self._connected_channels)
