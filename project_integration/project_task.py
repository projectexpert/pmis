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

import tools
from osv import fields, osv
from tools.translate import _

class task(osv.osv):
    _inherit = 'project.task'
    _description = "Activity"
                                
 

            
    _columns = {
        'name': fields.char('Summary', size=128, required=True),
        'state': fields.selection([('draft', 'Draft'),('ready','Ready to Start'),('open', 'In Progress'),('pending', 'Pending'), ('cancelled', 'Cancelled'), ('done', 'Done')], 'State', readonly=True, required=True,
                                  help='If the task is created the state is \'Draft\'.\n If the task is ready to start started, the state becomes \'Ready to Start\'.\n If the task is started, the state becomes \'In Progress\'.\n If review is needed the task is in \'Pending\' state.\
                                  \n If the task is over, the states is set to \'Done\'.'),                     
        }


    def do_ready(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'ready'})
        self.send_ready(cr, uid, ids)
        return True
    
    def send_ready(self, cr, uid, ids):

        task_br = self.browse(cr,uid,ids)
        for t in task_br:
            project = t.project_id
#            subject = _("Task '%s' is ready to start") % t.name
            if t.user_id and t.user_id.address_id and t.user_id.address_id.email:
                to_adr = t.user_id.address_id.email                
#                signature = t.user_id.signature
            else:
                raise osv.except_osv(_('Error'), _("Couldn't send mail because your email address is not configured!"))
#            
#            from_adr = tools.config.get('email_from', False) or t.user_id.address_id.email
#            
#            
#            task_name = u'Task name: %s' %(tools.ustr(t.name))
#            project_code = u'Project code: %s' %(tools.ustr(t.project_complete_wbs_name))
#            task_id = u'Task id: %s' %(tools.ustr(t.id))
#            
#            vals = [task_name, project_code, task_id]
#
#            
#            header = u'\n'.join(vals)
#            footer = ''
#            body = u'%s\n%s\n%s\n\n-- \n%s' % (header, t.description, footer, signature)
#            
#            mail_id = tools.email_send(from_adr, to_adr, subject, tools.ustr(body), email_bcc=[from_adr])
#                        
#            if not mail_id:
#                raise osv.except_osv(_('Error'), _("Couldn't send mail! Check the email ids and smtp configuration settings"))
            
#            msg_dict = {'new': 'Send', 'reply': 'Reply', 'forward': 'Forward'}
            
 #           self.history(cr, uid,[t], _(msg_dict['new']), history=True,email=to_adr, details=body,subject=subject, email_from=from_adr, message_id=None, references=None, attach=None)
            email_template_ids = self.pool.get('email.template').search(cr,uid,[('object_name.name','=','Task'),('name','=','Project task ready to start')],context=None)
            for email_template_id in email_template_ids:
                self.pool.get('email.template').generate_mail(cr,uid,email_template_id,ids,context=None)
            
        return {}    
    
    def write(self, cr, uid, ids, vals, *args, **kwargs):
        if isinstance(ids, (int, long)):
            ids = [ids]
        if vals.get('user_id', False):
            data_task = self.browse(cr, uid, ids)
            for tsk in data_task:
                old_user_id = tsk.user_id.id
                new_user_id = vals['user_id']
                if old_user_id <> new_user_id:
                    self.send_onchange_user_id(cr, uid, ids, vals['user_id'])
         
        return super(task,self).write(cr, uid, ids, vals, *args, **kwargs)

    def send_onchange_user_id(self, cr, uid, ids, user_id):
        
        user_obj=self.pool.get('res.users')
        user_br = user_obj.browse(cr,uid,[user_id])
        for usr in user_br:
            task_br = self.browse(cr,uid,ids)
            for t in task_br:
                project = t.project_id
                subject = _("Task '%s' has been assigned to you") % t.name
                if usr.id and usr.address_id and usr.address_id.email:
                    to_adr = usr.address_id.email                
                    signature = usr.signature
                else:
                    raise osv.except_osv(_('Error'), _("Couldn't send mail because your email address is not configured!"))
                
                from_adr = tools.config.get('email_from', False) or usr.address_id.email
                
                
                task_name = u'Task name: %s' %(tools.ustr(t.name))
                project_code = u'Project code: %s' %(tools.ustr(t.project_complete_wbs_name))
                task_id = u'Task id: %s' %(tools.ustr(t.id))
                
                vals = [task_name, project_code, task_id]
    
                
                header = u'\n'.join(vals)
                footer = ''
                body = u'%s\n%s\n%s\n\n-- \n%s' % (header, t.description, footer, signature)
                
                mail_id = tools.email_send(from_adr, to_adr, subject, tools.ustr(body), email_bcc=[from_adr])
                            
                if not mail_id:
                    raise osv.except_osv(_('Error'), _("Couldn't send mail! Check the email ids and smtp configuration settings"))
                
                msg_dict = {'new': 'Send', 'reply': 'Reply', 'forward': 'Forward'}
                
                self.history(cr, uid,[t], _(msg_dict['new']), history=True,email=to_adr, details=body,subject=subject, email_from=from_adr, message_id=None, references=None, attach=None)
                
        return {}    

    def do_close(self, cr, uid, ids, context=None):
        """
        Close Task
        """
        res = super(task,self).do_close(cr, uid, ids, context)
        
        project_task_obj=self.pool.get('project.task')
        
        l_task =self.browse(cr, uid, ids, context=context)
        for t in l_task:
            for child in t.child_ids:
                child_task_br = project_task_obj.browse(cr, uid, child.id, context=context)
                if child_task_br.state == 'draft':
                    project_task_obj.do_ready(cr, uid, [child.id])
                
        return True

task()

