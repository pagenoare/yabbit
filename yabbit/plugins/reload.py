

class Plugin(object):
    command = 'reload'

    def run(self, bot, *args):
        for plugin in bot.config.INSTALLED_PLUGINS:
            bot.plugin_manager.unload_plugin(plugin)
            bot.plugin_manager.load_plugin(plugin)