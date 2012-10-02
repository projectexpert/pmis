# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields,osv
from tools.translate import _
import binascii


class project_communications_mailgate(osv.osv):
    _name = "project.project"
    _inherit = ['mailgate.thread','project.project']
    
    _columns={
                'message_ids': fields.one2many('mailgate.message', 'res_id', 'Messages', domain=[('model','=',_name)], readonly=True),
              }
    
    def message_new(self, cr, uid, msg, context=None):
#        """
#        Automatically calls when new email message arrives
#
#        @param self: The object pointer
#        @param cr: the current row, from the database cursor,
#        @param uid: the current user’s ID for security checks
#        """
        res = {}
#        mailgate_obj = self.pool.get('email.server.tools')
#        subject = msg.get('subject')
#        body = msg.get('body')
#        msg_from = msg.get('from')
#        priority = msg.get('priority')

#        data = {      
#            'name': subject,
#            'description': body,
#        }
#        res = mailgate_obj.get_partner(cr, uid, msg_from)
#        if res:
#            data.update(res)
#        res = self.create(cr, uid, data)    
        
#        attachments = msg.get('attachments', [])
#        for attachment in attachments or []:
#            data_attach = {
#                'name': attachment,
#                'datas':binascii.b2a_base64(str(attachments.get(attachment))),
#                'datas_fname': attachment,
#                'description': 'Mail attachment',
#                'res_model': self._name,
#                'res_id': res,
#            }
#            self.pool.get('ir.attachment').create(cr, uid, data_attach)
#
        return res           
    
    def message_update(self, cr, uid, id, msg, data={}, context=None): 
        mailgate_obj = self.pool.get('email.server.tools')
        subject = data.get('subject')
        body = data.get('body')
        msg_from = data.get('from')
        msg_to = data.get('to')
        priority = data.get('priority')
        attachments = data.get('attachments', [])        

#      msg_actions, body_data = mailgate_obj.msg_act_get(msg)           
#       data.update({
#           'description': body_data,            
#       })
#       act = 'do_'+default_act
#       if 'state' in msg_actions:
#           if msg_actions['state'] in ['draft','close','cancel','open','pending']:
#               act = 'do_' + msg_actions['state']    

#       if 'priority' in msg_actions:
#           if msg_actions['priority'] in ('1','2','3','4','5'):
#               data['priority'] = msg_actions['priority']
#       
#       self.write(cr, uid, [id], data)
        msg_dict = {'new': 'Send', 'reply': 'Reply', 'forward': 'Forward'}
        self._history(cr, uid, id, _(msg_dict['new']), history=True, subject=subject, email=msg_to, details=body, email_from=msg_from, message_id=None, attach=attachments)
#       getattr(self,act)(cr, uid, [id])
        return {}    

    def message_followers(self, cr, uid, ids, context=None):
        res = []
        if isinstance(ids, (str, int, long)):
            select = [ids]
        else:
            select = ids
        for project in self.browse(cr, uid, select, context=context):
            user_email = (project.user_id and project.user_id.address_id and project.user_id.address_id.email) or False
            res += [(user_email, False, False, project.priority)]
        if isinstance(ids, (str, int, long)):
            return len(res) and res[0] or False
        return res

    def msg_send(self, cr, uid, id, *args, **argv):
        return True
    
    def _history(self, cr, uid, cases, keyword, history=False, subject=None, email=False, details=None, email_from=False, message_id=False, attach=[], context=None):
        mailgate_pool = self.pool.get('mailgate.thread')
        return mailgate_pool.history(cr, uid, cases, keyword, history=history,\
                                       subject=subject, email=email, \
                                       details=details, email_from=email_from,\
                                       message_id=message_id, attach=attach, \
                                       context=context)
        

project_communications_mailgate()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
