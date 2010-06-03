<!DOCTYPE html>
<html version="XHTML+RDFa 1.0" xmlns:tal="http://xml.zope.org/namespaces/tal" xmlns:mgd="http://www.midgard-project.org/midgard2/9.03">
    <head>
        <title>${ c.title }</title>
		
		${h.javascript_link('/midcom-static/fi.infigo.chat/jquery.js')}
		${h.javascript_link('/midcom-static/fi.infigo.chat/client.js')}
		${h.stylesheet_link('/midcom-static/fi.infigo.chat/chat.css')}
		
		${h.stylesheet_link('/midcom-static/midgardmvc_core/midgard/screen.css', media="screen,projection,tv")}
		${h.stylesheet_link('/midcom-static/midgardmvc_core/midgard/content.css')}
		${h.stylesheet_link('/midcom-static/midgardmvc_core/services/uimessages/simple.css')}
				
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
        <link rel="shortcut icon" href="${ h.url("/midcom-static/midgardmvc_core/midgard/midgard.ico") }" type="image/vnd.microsoft.icon" />

		<script type="text/javascript">
			jQuery(document).ready(function() {
				chat_client.init({
			        queue_path: "${h.url(controller="fi_infigo_chat/post", action="queue")}",
			        post_path: "${h.url(controller="fi_infigo_chat/post", action="new")}"
				});
				
				chat_client.poll();
			});
		</script>
    </head>
    <body mgd:type="midgard_page">
        <div id="container">
            <header>
                <div class="grouplogo">
                    <a href="/"><img src="${ h.url("/midcom-static/midgardmvc_core/midgard/midgard.gif") }" alt="Midgard" width="135" height="138" /></a>
                </div>
            </header>
            <section id="content">				
                <!-- beginning of content-text -->
                <div id="content-text">
                    ${next.body()}
                </div>
            </section>
        </div>
        <footer>
             <a href="http://www.midgard-project.org/" rel="powered">Midgard CMS</a> power since 1999. 
             <a href="http://www.gnu.org/licenses/lgpl.html" rel="license" about="http://www.midgard-project.org/">Free software</a>.
        </footer>
    </body>
</html>