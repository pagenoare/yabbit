from . import BasePlugin


class Plugin(BasePlugin):
    command = ':ping'

    def execute(self, accessor, user, channel, data):
        user, _ = self.split_user(user)
        to = channel or user
        accessor.msg(to, '%s: :pong' % user)
