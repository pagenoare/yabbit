from twisted.internet import protocol
from twisted.internet import reactor

from . import config
from .plugin import PluginManager
from .yabbit import Yabbit


class YabbitFactory(protocol.ClientFactory):

    def __init__(self, network):
        self.network = network

    def buildProtocol(self, addr):
        """
        Build a protocol (initialize main Bot class).
        """
        return Yabbit(self)

    def clientConnectionLost(self, connector, reason):
        """
        Connection lost, try to reconnect.
        """
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        """
        Connection failed, print the reason and exit.
        """
        print 'connection failed: {}'.format(reason)
        reactor.stop()


def main():
    load_plugins()
    setup_networks_connections()
    reactor.run()


def load_plugins():
    plugin_manager = PluginManager()
    for plugin_name in config.INSTALLED_PLUGINS:
        plugin_manager.load(plugin_name)


def setup_networks_connections():
    for network, settings in config.NETWORKS.items():
        reactor.connectTCP(
            settings['host'], settings.get('port', 6667),
            YabbitFactory(network)
        )

if __name__ == '__main__':
    main()
