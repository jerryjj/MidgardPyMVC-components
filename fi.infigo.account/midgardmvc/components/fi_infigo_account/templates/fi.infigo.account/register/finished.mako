<%inherit file="/base/default.mako" />

<%def name="body()">
	<h1>${ _("Finished") }</h1>

	<p>
		Firstname: ${ c.person.firstname }<br />
		Lastname: ${ c.person.lastname }<br />
		
		% if not c.hide_email:
		Email: ${ c.person.email }<br />
		% endif
	</p>
	<p>	
		Username: ${ c.user.login }<br />
	</p>
	
</%def>