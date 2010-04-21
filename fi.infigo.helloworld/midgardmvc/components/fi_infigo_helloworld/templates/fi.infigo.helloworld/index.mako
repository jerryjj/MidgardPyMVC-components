<%inherit file="/base/default.mako" />

<%def name="body()">

${h.javascript_link('/midcom-static/fi.infigo.helloworld/test.js')}

Hello, 
% if c.user:
	${c.user.login}
% else:
	world!
% endif

</%def>