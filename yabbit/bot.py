import logging
from twisted.words.protocols import irc

import config
from plugin import PluginManager

log = logging.getLogger(__name__)


class Yabbit(irc.IRCClient):

    def __init__(self):
        self.plugin_manager = PluginManager()
        self.config = config
        log.debug('Initialized Yabbit class.')
        # Load plugins
        for module in self.config.INSTALLED_PLUGINS:
            log.info('Loading plugin: {}'.format(module))
            self.plugin_manager.load_plugin(module)
            log.debug('Loaded plugin: {}'.format(module))

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
        # Join channels
        for channel in self.factory.channels:
            log.info('Joining channel: {}'.format(channel))
            self.join(channel)

    def privmsg(self, user, channel, msg):
        """
        Runs plugins when command defined in plugin class has been sent
        (directly or on a channel)
        """
        nickname, hostmask = user.split('!', 1)

        if msg.startswith(self.config.COMMAND_CHAR):
            log.info(
                'Received string which seems to be command: {}'.format(msg)
            )
            msg = msg.replace(self.config.COMMAND_CHAR, '').split()
            if not msg:
                return

            plugins = self.plugin_manager.get_plugins_by_command(msg[0])
            for plugin in plugins:
                plugin.execute(self, nickname, hostmask, channel, msg)

    def handleCommand(self, command, prefix, params):
        irc.IRCClient.handleCommand(self, command, prefix, params)
        plugins = self.plugin_manager.get_plugins_by_event(command.lower())
        for plugin in plugins:
            plugin.execute(self, params, command, prefix)
