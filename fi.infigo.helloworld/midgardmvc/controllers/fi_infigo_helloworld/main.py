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
        c.page = h.midgard.mgdschema.midgard_page()
        page_found = c.page.get_by_path('/midcom_root')
        
        if page_found:
            c.title += ":: " + c.page.title
        else:
            c.title += ":: " + _("Frontpage")
        
        c.user = get_active_user()
        c.person = get_active_user_person()
        print c.person
        return render('fi.infigo.helloworld/index.mako')
