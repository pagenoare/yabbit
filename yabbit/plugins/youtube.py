
class Plugin(object):
    command = ['yt', 'youtube']

    def privmsg(self, bot, params, command, prefix):
        # [regexp] check if msg contain URL
        # check if url is YT url (this one gonna be tricky)
        # fetch URL title
        print command, prefix, params

    def run(self):
        # get args (this should be passed)
        # search though YT
        pass
