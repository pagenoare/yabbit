import logging

from twisted.internet import reactor, protocol

import config
from bot import Yabbit

log = logging.getLogger(__name__)


class YabbitFactory(protocol.ClientFactory):

    def __init__(self, channels):
        """
        Initialize Factory
        :param channels: List of channels passed to bot to join after connecting
        to network.
        """
        self.nickname = 'yabbit'
        self.channels = channels
        log.debug('Initialized Yabbit Factory')

    def buildProtocol(self, addr):
        """
        Build a protocol (initialize main Bot class).
        """
        yabbit = Yabbit()
        yabbit.factory = self
        return yabbit

    def clientConnectionLost(self, connector, reason):
        """
        Connection lost, try to reconnect.
        """
        connector.connect()
        log.debug('Connection lost. Trying to reconnect...')

    def clientConnectionFailed(self, connector, reason):
        """
        Connection failed, print the reason and exit.
        """
        log.error('Connection failed. Reason: {}'.format(reason))
        reactor.stop()


if __name__ == '__main__':
    factory = YabbitFactory(config.CHANNELS)
    reactor.connectTCP(config.NETWORK, config.PORT, factory)
    reactor.run()