<%inherit file="/base/default.mako" />

<%def name="body()">

Hello, 
% if c.user:
	${c.user.login}
% else:
	world!
% endif

<p>${ h.link_to(_("Link to this page"), h.url(controller="fi_infigo_account/main", action="index")) }</p>

</%def>