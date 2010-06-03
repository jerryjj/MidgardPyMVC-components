import logging
log = logging.getLogger(__name__)

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.i18n.translation import _

from midgardmvc.lib.base import BaseController, render
import midgardmvc.lib.helpers as h

from midgardmvc.lib.midgard.auth import get_active_user, get_active_user_person

class ProfileController(BaseController):
    
    def index(self):
        return redirect(url(controller="fi_infigo_account/profile", action="view"))
    
    def view(self):
        c.title += ":: " + _("View")
        
        return render('fi.infigo.account/profile/view.mako')
        
    def edit(self):
        c.title += ":: " + _("Edit")
        
        return render('fi.infigo.account/profile/edit.mako')