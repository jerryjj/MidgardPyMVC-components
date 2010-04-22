<%inherit file="/fi.infigo.chat/layout.mako" />

<%def name="body()">

<div id="chat_holder">
	<div id="message_queue">
		<ul>
		</ul>
	</div>
	<div id="input">
		<form action="${h.url(controller="fi_infigo_chat/post", action="new")}" method="post" id="chat_form">
			<table>
				<tr>
					<td><input name="content" id="message_input" style="width:500px"/></td>
					<td style="padding-left:5px">
						<input type="submit" value="${ _("Send") }"/>
					</td>
				</tr>
			</table>
		</form>
	</div>
</div>

</%def>