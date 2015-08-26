openerp.sync_mail_forward = function (instance) {
	var mail = instance.mail;

	mail.ThreadComposeMessage.include({
		on_compose_fullmail: function (default_composition_mode) {
			debugger;
            var self = this;
            if(!this.do_check_attachment_upload()) {
                return false;
            }
            var recipient_done = $.Deferred();
            if (this.is_log) {
                recipient_done.resolve([]);
            }
            else {
                recipient_done = this.check_recipient_partners();
            }
            $.when(recipient_done).done(function (partner_ids) {
                var context = {
                    'default_parent_id': self.id,
                    'default_body': mail.ChatterUtils.get_text2html(self.$el ? (self.$el.find('textarea:not(.oe_compact)').val() || '') : ''),
                    'default_attachment_ids': _.map(self.attachment_ids, function (file) {return file.id;}),
                    'default_partner_ids': partner_ids,
                    'default_is_log': self.is_log,
                    'mail_post_autofollow': true,
                    'mail_post_autofollow_partner_ids': partner_ids,
                    'is_private': self.is_private,
                };
                if (default_composition_mode != 'reply' && self.context.default_model && self.context.default_res_id) {
                    context.default_model = self.context.default_model;
                    context.default_res_id = self.context.default_res_id;
                }
                if (self.context.option == 'forward'){
                    context['option'] = 'forward';
                }
                var action = {
                    type: 'ir.actions.act_window',
                    res_model: 'mail.compose.message',
                    view_mode: 'form',
                    view_type: 'form',
                    views: [[false, 'form']],
                    target: 'new',
                    context: context,
                };
                self.do_action(action);
                self.on_cancel();
            });
        }
	});

    mail.ThreadMessage.include({
        bind_events: function () {
            var self = this;
            this._super.apply(this, arguments);
            this.$('.oe_forward').on('click', this.on_message_forward);
        },
        on_message_forward:function (event) {
            event.stopPropagation();
            this.create_thread();
            this.thread.on_compose_message(event);
            this.thread.compose_message.context['option'] = 'forward';
            return false;
        },
        on_message_reply:function (event) {
            var self = this;
            this._super.apply(this, arguments);
            this.thread.compose_message.context['option'] = 'reply';
            return false;
        }
    });
};