from routes.route import Route
import os
from pylons.i18n.translation import _

from midgardmvc.components.base import ComponentBase

class AccountComponent(ComponentBase):
    __name__ = __name__
    __routes__ = [
        Route(None, "/", controller="fi_infigo_account/main", action="index"),
        Route(None, "/register", controller="fi_infigo_account/main", action="register"),
        Route(None, "/register/{phase}", controller="fi_infigo_account/main", action="register"),
        Route(None, "/register/{phase}/{guid}", controller="fi_infigo_account/main", action="register"),
        Route(None, "/profile/{action}", controller="fi_infigo_account/profile"),
    ]
    __routes_prefix__ = "/account"
    
    def initialize(self):
        pass

def make_component(component_config=None):
    return AccountComponent(config=component_config)