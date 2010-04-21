from routes.route import Route
import os
from pylons.i18n.translation import _

from midgardmvc.components.base import ComponentBase

class HelloWorldComponent(ComponentBase):
    __routes__ = [
        Route(None, "/", controller="fi_infigo_helloworld/main", action="index"),
        Route(None, "/index", controller="fi_infigo_helloworld/main", action="index")
    ]
    __routes_prefix__ = "/HelloWorld"
    
    def initialize(self):
        self.component_root = os.path.dirname(os.path.abspath(__file__))
        self.__config_dir__ = os.path.join(self.component_root, 'config')
        self.__templates_dir__ = os.path.join(self.component_root, 'templates')
        self.__static_files__ = os.path.join(self.component_root, 'public')
        
    def say(self):
        print _("Hello, World!")

def make_component(component_config=None):
    return HelloWorldComponent(config=component_config)