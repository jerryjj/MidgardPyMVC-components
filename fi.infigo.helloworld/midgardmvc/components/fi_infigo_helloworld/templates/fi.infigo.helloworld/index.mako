<%inherit file="/base/default.mako" />

<%def name="body()">

Hello, 
% if c.user:
	${c.user.login}
% else:
	world!
% endif

<p>${ h.link_to(_("Link to this page"), h.url(controller="fi_infigo_helloworld/main", action="index")) }</p>

${h.javascript_link('/midcom-static/fi.infigo.helloworld/test.js')}

</%def>