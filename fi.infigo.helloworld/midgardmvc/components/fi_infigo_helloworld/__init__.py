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
        component_root = os.path.dirname(os.path.abspath(__file__))
        self.__templates_dir__ = os.path.join(component_root, 'templates')
    
    def say(self):
        print _("Hello, World!")

def make_component(component_config=None):
    return HelloWorldComponent(config=component_config)