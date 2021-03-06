from sapp.plugins.celery.plugin import CeleryPlugin
from sapp.plugins.json import JsonPlugin
from sapp.plugins.logging import LoggingPlugin
from sapp.plugins.pyramid.configurator import ConfiguratorWithPyramid
from sapp.plugins.pyramid.plugins import RoutingPlugin
from sapp.plugins.settings import SettingsPlugin
from sapp.plugins.sqlalchemy.plugin import DatabasePlugin
from sapp.plugins.tornado.configurator import TornadoConfigurator
from sapp.plugins.tornado.plugin import TornadoPlugin

from example.application.capp import cel
from example.application.routing import ExampleRouting


class ExampleConfigurator(ConfiguratorWithPyramid, TornadoConfigurator):
    def append_plugins(self):
        self.add_plugin(SettingsPlugin("example.application.settings"))
        self.add_plugin(LoggingPlugin())
        self.add_plugin(JsonPlugin())

        self.add_plugin(RoutingPlugin(ExampleRouting))
        self.add_plugin(DatabasePlugin("dbsession"))
        self.add_plugin(CeleryPlugin(cel))
        self.add_plugin(TornadoPlugin())
