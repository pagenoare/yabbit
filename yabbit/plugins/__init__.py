accessible_network_accessors = {}


class BasePlugin(object):
    def split_user(self, user):
        return user.split('!', 1)

    def execute(self, accessor, user, channel, data):
        pass
