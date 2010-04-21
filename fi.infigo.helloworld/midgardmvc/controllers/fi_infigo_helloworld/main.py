import logging
log = logging.getLogger(__name__)

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.i18n.translation import _

from midgardmvc.lib.base import BaseController, render
import midgardmvc.lib.helpers as h

from midgardmvc.lib.midgard.auth import get_active_user, get_active_user_person

class MainController(BaseController):
    
    def index(self):
        c.title += ":: " + _("HelloWorld")
        
        c.user = get_active_user()
        c.person = get_active_user_person()
        
        return render('fi.infigo.helloworld/index.mako')
