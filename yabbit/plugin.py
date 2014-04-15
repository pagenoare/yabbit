from importlib import import_module
import logging
import sys

from .users import UserManager

logger = logging.getLogger(__name__)


class PluginError(Exception):
    pass


class PluginManager(object):
    plugins = []
    package_name = 'plugins'
    permitted_events = (
        'privmsg', 'noticed', 'user_joined', 'user_left',
        'user_quit', 'user_kicked', 'action', 'topic_updated'
    )

    @classmethod
    def load(cls, plugin_name):
        """
        Method used to load plugin
        """
        plugins = cls.plugins
        plugins_names = (cls._plugin_name(plugin) for plugin in plugins)
        if plugin_name in plugins_names:
            return

        try:
            module = import_module(
                '{}.{}'.format(cls.package_name, plugin_name)
            )
        except ImportError:
            logger.error('{} couldn\'t be found. '.format(plugin_name),
                         exc_info=True)
        else:
            cls.plugins.append(module.Plugin())

    @classmethod
    def _plugin_name(cls, plugin):
        return plugin.__module__.rsplit('.')[-1]

    @classmethod
    def unload(cls, plugin_name):
        """
        Method used to unload specified plugin
        """
        try:
            plugin = [
                plugin for plugin in cls.plugins
                if cls._plugin_name(plugin) == plugin_name
            ][0]
        except IndexError:
            logger.error('unload called with not loaded plugin name:'
                         ' %s' % plugin_name)
        else:
            if plugin:
                index = cls.plugins.index(plugin)
                del cls.plugins[index]
                del sys.modules[plugin.__module__]

    @classmethod
    def dispatch(cls, protocol, event, user, *args, **kwargs):
        if event not in cls.permitted_events:
            return
        for plugin in cls.plugins:
            try:
                method = getattr(plugin, event, None)
                if not method:
                    method = getattr(plugin, 'dispatch', None)
                    kwargs['event'] = event
                if not method and event == 'privmsg' and hasattr(
                        plugin, 'command'):
                    channel, data = args
                    command = data.split(None, 1)[0]
                    if getattr(plugin, 'command') == command:
                        method = getattr(plugin, 'execute')
                        if not method:
                            raise PluginError(
                                'Plugin %s have "command" defined but have not '
                                'defined "execute" method' %
                                cls._plugin_name(plugin)
                            )
                            continue

                if cls._check_permissions(user, plugin, event):
                    method(protocol.accessor, user, *args, **kwargs)
                else:
                    logger.debug('No permission for %s on %s' %
                                 (event, plugin.__class__.__name__))
            except Exception as e:
                logger.warning(
                    'Exception when handling event "%s" by plugin "%s": %s' %
                    (event, cls._plugin_name(plugin), str(e)), exc_info=True)

    @staticmethod
    def _check_permissions(user, plugin, event):
        permission = getattr(plugin, 'permission', None)
        if not permission and event in ('privmsg', 'noticed', 'topic'):
            return True
        return UserManager().has_permission(user, permission)
