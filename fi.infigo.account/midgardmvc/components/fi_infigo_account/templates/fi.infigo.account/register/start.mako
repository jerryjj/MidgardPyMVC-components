<%inherit file="/base/default.mako" />

<%def name="body()">
	<h1>${ _("Register") }</h1>
	
	${h.form(h.url(controller="fi_infigo_account/main", action='register', phase=c.phase), method='post')}
		<div>
			<label>Firstname:</label> ${h.text('firstname', "")}
		</div>
		<div>
			<label>Lastname:</label> ${h.text('lastname', "")}
		</div>
		
		<div>
			<label>Homepage:</label> ${h.text('homepage', "")}
		</div>
		
		% if not c.hide_email:
		<div>
			<label>Username:</label> ${h.text('login', "")}
		</div>
		<div>
			<label>Email:</label> ${h.text('email', "")}
		</div>
		% else:
		<div>
			<label>Username and email:</label> ${h.text('login', "")}
		</div>
		% endif
		
		${h.submit('submit', _("Register"))}
	${h.end_form()}
</%def>