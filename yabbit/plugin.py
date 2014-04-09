import sys
from collections import namedtuple
from importlib import import_module

Plugin = namedtuple('Plugin', ['plugin_name', 'module', 'command', 'execute'])


class PluginManager(object):
    loaded_plugins = []

    def __init__(self, package_name='plugins'):
        self.package_name = package_name

    def load_plugin(self, plugin_name):
        """
        Method used to load plugin
        """
        try:
            module = import_module(
                '{}.{}'.format(self.package_name, plugin_name)
            )
        except ImportError:
            print '{} couldn\'t be found. '.format(plugin_name)
            return

        plugin = module.Plugin()
        self.loaded_plugins.append(
            Plugin(plugin_name, module, plugin.command, plugin.run)
        )

    def unload_plugin(self, plugin_name):
        """
        Method used to unload specified plugin
        """
        plugin = [
            plugin for plugin in self.loaded_plugins
            if plugin.plugin_name == plugin_name
        ]

        if plugin:
            index = self.loaded_plugins.index(plugin[0])
            del self.loaded_plugins[index]
            del sys.modules[plugin[0].module.__name__]

    def get_plugin_by_command(self, command):
        """
        This method returns plugin based on specified command
        """
        plugin = [
            plugin for plugin in self.loaded_plugins
            if plugin.command == command
        ]

        if plugin:
            return plugin[0]
