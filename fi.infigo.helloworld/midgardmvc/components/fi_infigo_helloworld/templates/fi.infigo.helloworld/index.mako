<%inherit file="/base/default.mako" />

<%def name="body()">

Hello, 
% if c.user:
	${c.user.login}
% else:
	world!
% endif

</%def>