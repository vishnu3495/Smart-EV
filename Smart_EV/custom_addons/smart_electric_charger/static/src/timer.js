//openerp.my_custom_module = function (instance){
//
//	instance.web.form.MyCustomWidget = instance.web.form.AbstractField.extend(instance.web.form.ReinitializeFieldMixin,
//        {
//            init: function(field_manager, node) {
//                this._super.apply(this, arguments);
//        },
//        start: function() {
//        	var self = this;
//            this._super.apply(this, arguments);
//            this.field_manager.on("view_content_has_changed", this, function () {
//            	// your logic goes here
//            });
//        },
//        startTimeCounter: function(){
//            var self = this;
//            clearTimeout(this.timer);
//            if (self.duration) {
//                this.duration -= 1;
//                this.timer = setTimeout(function() {
//                	// your logic goes here
//                }, 1000);
//                this.$el.html($('<span>' +self.secondsToDhms(self.duration) + '</span>'));
//            }
//            else {
//            	this.$el.html($('<span>' +self.secondsToDhms(0.0) + '</span>'));
//            }
//        },
//        secondsToDhms: function(seconds) {
//        	seconds = Number(seconds);
//        	var d = Math.floor(seconds / (3600*24));
//        	var h = // your logic goes here for hours
//        	var m = // your logic goes here for min
//        	var s = // your logic goes here for sec
//
//        	var dDisplay = d >= 0 ? "<span style='font-family: Consolas;font-size:24px;letter-spacing: .25em'>"+("0" + d).slice(-2)+"</span>":"";
//        	// your logic goes here for hours
//        	// your logic goes here for min
//        	// your logic goes here for sec
//        	return dDisplay +"<span style='font-family: Consolas;font-size:18px;letter-spacing: .50em'>:</span>"+hDisplay+"<span style='font-family: Consolas;font-size:18px;letter-spacing: .50em'>:</span>"+ mDisplay +"<span style='font-family: Consolas;font-size:18px;letter-spacing: .50em'>:</span>"+ sDisplay;
//        	},
//
//        updateValue: function() {
//            this._super.apply(this, arguments);
//            var self = this;
//            this.duration;
//            if (self.get("effective_readonly")) {
//            	// your logic goes here
//            	var model = new instance.web.Model(this.view.model);
//            	model.call("calc_time_js", [[this.view.datarecord.id]], {context: new instance.web.CompoundContext()}).then(function(result)
//                {
//                // your logic goes here
//                }
//                });
//            	this.$el.html($('<span>' +self.secondsToDhms(0.0) + '</span>'));
//            }
//        },
//    });
//    openerp.web.form.widgets.add('time_counter', 'instance.web.form.MyCustomWidget');
//};
//
