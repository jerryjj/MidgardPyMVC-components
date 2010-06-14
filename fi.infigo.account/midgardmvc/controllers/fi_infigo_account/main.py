import logging
log = logging.getLogger(__name__)

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.i18n.translation import _

from midgardmvc.lib.base import BaseController, render
import midgardmvc.lib.helpers as h

from midgardmvc.lib.midgard.auth import get_active_user, get_active_user_person
from midgardmvc.lib.midgard.auth import prepare_password

import midgardmvc.components.fi_infigo_account.lib.helpers as account_helpers

from pylons.decorators import validate
import formencode

from turbomail import Message

import midgardmvc.model.midgard.person
class RegistrationForm(midgardmvc.model.midgard.person.FormSchema):
    allow_extra_fields = True
    filter_extra_fields = False
    
    if request.environ["pylons.routes_dict"].get("phase", None) == "start":
        firstname = formencode.validators.String(not_empty=True)
        lastname = formencode.validators.String(not_empty=True)
        homepage = formencode.validators.String(not_empty=False)
        
        if not request.environ["fi.infigo.account"].config["registration"].get("username_is_email", False):
            email = formencode.validators.Email()        
            login = formencode.validators.String(not_empty=True)
        else:
            login = formencode.validators.Email(not_empty=True)

def resolveRegistrationForm():
    custom_schema = request.environ["fi.infigo.account"].config["registration"].get("schema", None)
    if custom_schema:
        from repoze.who.utils import resolveDotted
        klass = resolveDotted(custom_schema)
        
        return klass()
        
    return RegistrationForm()

class MainController(BaseController):
    
    def index(self):
        c.title += ":: " + _("Account")
        
        c.user = get_active_user()
        c.person = get_active_user_person()
        
        return render('fi.infigo.account/index.mako')
    
    @validate(schema=resolveRegistrationForm(), form='register')
    def register(self, phase=None, guid=None):
        c.title += ":: " + _("Register")
        
        # from midgardmvc.model.midgard import resolveSchemaFields
        # print resolveSchemaFields(h.midgard.mgdschema.midgard_person)
        
        c.hide_email = request.environ["fi.infigo.account"].config["registration"].get("username_is_email", False)
        
        if phase == "start":
            c.next_phase = "preview"
            view_tpl = 'fi.infigo.account/register/start.mako'
            
            if hasattr(self, 'form_result') and not hasattr(self, 'form_errors'):
                session["fi.infigo.account.registration_data"] = self.form_result
                session.save()
                
                h.flash_ok(_("Form saved successfully!"))
                redirect(url(controller="fi_infigo_account/main", action="register", phase=c.next_phase))
        elif phase == "preview":
            c.next_phase = "finished"
            view_tpl = 'fi.infigo.account/register/preview.mako'
            
            if not "fi.infigo.account.registration_data" in session:
                h.flash_alert(_("Fill in the registration form first!"))
                redirect(url(controller="fi_infigo_account/main", action="register", phase="start"))
            
            c.registration_data = session["fi.infigo.account.registration_data"]
            
            if request.POST and request.POST['continue']:
                user, person = self._createUser(c.registration_data, phase)
                redirect(url(controller="fi_infigo_account/main", action="register", phase=c.next_phase, guid=user.guid))
        elif phase == "finished":
            c.next_phase = None
            view_tpl = 'fi.infigo.account/register/finished.mako'
            
            if not guid:
                h.flash_alert(_("Error while processing request!"))
                redirect(url(controller="fi_infigo_account/main", action="register", phase="start"))
            
            qb = h.midgard.query_builder('midgard_user')
            qb.add_constraint("guid", "=", guid)            
            res = qb.execute()
            
            if not len(res) > 0:
                h.flash_alert(_("Error while processing request!"))
                redirect(url(controller="fi_infigo_account/main", action="register", phase="start"))
            
            c.user = res[0]
            
            c.person = c.user.get_person()
        else:
            redirect(url(controller="fi_infigo_account/main", action="register", phase="start"))
        
        c.phase = phase
        
        return render(view_tpl)
    
    def _createUser(self, data, phase, auto_login=True):
        person = h.midgard.mgdschema.midgard_person()
        person.firstname = data.get("firstname", "").encode('utf-8')
        person.lastname = data.get("lastname", "").encode('utf-8')
        person.email = data.get("email", "").encode('utf-8')
        
        try:
            person.create()
            log.debug("Person created with GUID: %s" % person.guid)
        except:
            mgd_error_str = h.midgard._connection.get_error_string()
            log.error("Could not create person, reason: %s" % mgd_error_str)
            
            h.flash_alert(
                _("Could not create <%(object_type)s object>, reason: %(mgd_reason)s") % {'object_type': "Person", 'mgd_reason': mgd_error_str}
            )
            
            redirect(url(controller="fi_infigo_account/main", action="register", phase=phase))
        
        user = h.midgard.db.user()
        user.login = data.get("login").encode('utf-8')
        password = account_helpers.generatePassword(8)
        user.password = prepare_password(password, "Plaintext")
        user.authtype = "Plaintext"
        user.active = True
        
        try:
            user.create()
            log.debug("User created with GUID: %s" % user.guid)
        except:
            mgd_error_str = h.midgard._connection.get_error_string()
            log.error("Could not create user, reason: %s" % mgd_error_str)
            
            h.flash_alert(
                _("Could not create <%(object_type)s object>, reason: %(mgd_reason)s") % {'object_type': "User", 'mgd_reason': mgd_error_str}
            )
            
            redirect(url(controller="fi_infigo_account/main", action="register", phase=phase))
        
        status = user.set_person(person)
        if not status:
            h.flash_alert(
                _("Failed assigning person to user object, reason: %(mgd_reason)s") % {'mgd_reason': h.midgard._connection.get_error_string()}
            )
            
            redirect(url(controller="fi_infigo_account/main", action="register", phase=phase))
        
        if auto_login:
            user.log_in()

            if request.environ["fi.infigo.account"].config["registration"].get("send_login_info_by_email", True):
                message_content = ''
                message_content += _("Your login details") + "\n"
                message_content += _("Login:") + user.login
                message_content += "\n"
                message_content += _("Password:") + user.login
                message = Message(request.environ["fi.infigo.account"].config["email"].get("default_sender"), person.email, _("Registration details"))
                message.plain = message_content
                try:
                    status = message.send()
                except Exception, e:
                    h.flash_alert(_("Failed sending mail, reason: %(reason)s") % {'reason': e})

        return [user, person]