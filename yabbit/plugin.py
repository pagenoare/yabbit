import sys
from collections import namedtuple
from importlib import import_module

Plugin = namedtuple(
    'Plugin', ['plugin_name', 'module', 'events', 'command', 'execute']
)

ALLOWED_EVENTS = [
    'privmsg',
    'join',
    'part',
    'quit',
    'kick',
    'action',
    'topic',
    'nick',
    'invite',
]


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

        events = {}
        for event in ALLOWED_EVENTS:
            if hasattr(plugin, event):
                events[event] = getattr(plugin, event)

        self.loaded_plugins.append(
            Plugin(
                plugin_name,
                module,
                events,
                plugin.command,
                plugin.run
            )
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

    def get_plugins_by_command(self, command):
        """
        This method returns plugin based on specified command
        """
        plugins = [
            plugin for plugin in self.loaded_plugins
            if plugin.command == command
        ]

        return plugins

    def get_plugins_by_event(self, event):
        for plugin in self.loaded_plugins:
            if event in plugin.events:
                yield plugin._replace(execute=plugin.events.get(event))
