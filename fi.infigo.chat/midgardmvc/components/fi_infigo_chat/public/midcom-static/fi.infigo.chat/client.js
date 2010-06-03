jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
	    json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

jQuery.fn.disable = function() {
    this.enable(false);
    return this;
};

jQuery.fn.enable = function(opt_enable) {
    if (arguments.length && !opt_enable) {
        this.attr("disabled", "disabled");
    } else {
        this.removeAttr("disabled");
    }
    return this;
};

jQuery.postJSON = function(url, args, callback, error_callback) {
    jQuery.ajax({url: url, data: jQuery.param(args), dataType: "text", type: "POST",
        success: function(response) {
            callback(response);
    }, error: error_callback});
}

var clientBase = function() {
    var _config = {
        error_sleep_time: 500,
        queue_path: null,
        post_path: null,        
        form_path: '#chat_form'
    };
    
    var _errorSleepTime = 500;
    
    var _cursor = null;
    
    var _newUpdate = function(response)
    {
        if (response == "") { return; }
        
        data = null;
        
        try {
            data = eval("(" + response + ")")
        } catch (e) {
            //console.log("Unable to eval response!");
        }
        
        if (data == null) { return; }
        
        if (data.length) {
            jQuery.each(data, function(i, resp) {
                _showMessage(resp.content);
            });
        } else if (data.content) {
            _showMessage(data.content);
        }
    };
    
    var _showMessage = function(message)
    {
        item = jQuery("<li />").html(message);
        item.appendTo(jQuery("#message_queue ul"));
    };
    
    return {
        init: function(config)
        {
            _config = jQuery.extend(_config, config || {});
            
            _errorSleepTime = _config.error_sleep_time;
            
            this._register_form();
        },
        _register_form: function()
        {
            var self = this;
            
            jQuery(_config.form_path).live("submit", function() {
        	    self.handleMessageForm($(this));
        	    return false;
            });
            
            jQuery(_config.form_path).live("keypress", function(e) {
            	if (e.keyCode == 13) {
            	    self.handleMessageForm($(this));
            	    return false;
            	}
            });
            
            jQuery("#message_input").select();
        },
        handleMessageForm: function(form)
        {
            var message = form.formToDict();
            var disabled = form.find("input[type=submit]");
            disabled.disable();
            
            self = this
            
            jQuery.postJSON(_config.post_path, message, function(response) {
    	        form.find("input[type=text]").val("").select();
    	        disabled.enable();
            });
        },
        poll: function()
        {
            if (! _config.queue_path) {
                return;
            }
            
            var args = {cursor: 0};
            if (_cursor) args.cursor = _cursor;
            
            var self = this;
            
            jQuery.ajax({url: _config.queue_path, data: jQuery.param(args), dataType: "text", type: "GET",
                success: function(response) {
                    self.gotUpdates(response);
            }, error: self.onError});
        },
        onError: function(response)
        {
            _errorSleepTime *= 2;
            // console.log("Poll error; sleeping for", _errorSleepTime, "ms");
            // console.log(response);
            window.setTimeout("rePoll()", _errorSleepTime);
        },
        gotUpdates: function(updates)
        {
            _newUpdate(updates);
            
            _errorSleepTime = _config.error_sleep_time;
            window.setTimeout("rePoll()", 400);
        }
    }
}

chat_client = new clientBase();

function rePoll()
{
    chat_client.poll();
}

