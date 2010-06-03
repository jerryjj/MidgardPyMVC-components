import logging
log = logging.getLogger(__name__)

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.i18n.translation import _

from midgardmvc.lib.base import BaseController, render
import midgardmvc.lib.helpers as h

class MainController(BaseController):
    
    def index(self):
        c.title += ":: " + _("Chat")
        
        return render('fi.infigo.chat/index.mako')
