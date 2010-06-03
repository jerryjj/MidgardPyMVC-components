from routes.route import Route
import os
from pylons.i18n.translation import _

from midgardmvc.components.base import ComponentBase

class ChatComponent(ComponentBase):
    __name__ = __name__
    __routes__ = [
        Route(None, "/", controller="fi_infigo_chat/main", action="index"),
        Route(None, "/index", controller="fi_infigo_chat/main", action="index"),
        Route(None, "/post/new", controller="fi_infigo_chat/post", action="new"),
        Route(None, "/post/queue", controller="fi_infigo_chat/post", action="queue"),
    ]
    __routes_prefix__ = "/chat"
    
    def initialize(self):
        pass

def make_component(component_config=None):
    return ChatComponent(config=component_config)