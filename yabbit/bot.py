from importlib import import_module
from twisted.words.protocols import irc

import config
from plugin import PluginManager


class Yabbit(irc.IRCClient):

    def __init__(self):
        self.plugin_manager = PluginManager()
        self.config = config

    @property
    def nickname(self):
        """
        Returns bot's nickname
        """
        return self.factory.nickname

    @property
    def channels(self):
        """
        Returns list of channels
        """
        return self.factory.channels

    def signedOn(self):
        """
        Actions which will be executed after connecting to a server
        """
        # Load plugins
        for module in self.config.INSTALLED_PLUGINS:
            self.plugin_manager.load_plugin(module)

        # Join channels
        for channel in self.factory.channels:
            self.join(channel)

    def privmsg(self, user, channel, msg):
        """
        Runs plugins when command defined in plugin class has been sent
        (directly or on a channel)
        """
        nickname, hostmask = user.split('!', 1)

        if msg.startswith(self.config.COMMAND_CHAR):
            msg = msg.replace(self.config.COMMAND_CHAR, '').split()
            if not msg:
                return

            plugin = self.plugin_manager.get_plugin_by_command(msg[0])
            if plugin:
                plugin.execute(self, nickname, hostmask, channel, msg)
