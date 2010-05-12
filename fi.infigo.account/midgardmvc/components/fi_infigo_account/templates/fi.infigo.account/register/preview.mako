<%inherit file="/base/default.mako" />

<%def name="body()">
	<h1>${ _("Preview") }</h1>
	
	${h.form(h.url(controller="fi_infigo_account/main", action='register', phase=c.phase), method='post')}
		<div>
			<label>Firstname:</label> ${c.registration_data.get("firstname", "")}
		</div>
		<div>
			<label>Lastname:</label> ${c.registration_data.get("lastname", "")}
		</div>
		<div>
			<label>Username:</label> ${c.registration_data.get("login", "")}
		</div>
	
		% if not c.hide_email:
		<div>
			<label>Email:</label> ${c.registration_data.get("email", "")}
		</div>
		% endif
	
		${h.submit('continue', _("Continue"))}
	${h.end_form()}
</%def>