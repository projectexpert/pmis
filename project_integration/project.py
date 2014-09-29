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

from openerp.osv import fields, osv
from openerp.tools.translate import _

    
class project(osv.osv):
    _name = "project.project"
    _inherit = "project.project"
 
    _columns = {        
        'predecessor_ids': fields.many2many('project.project', 'projects_relationships', 'project_id', 'predecessor_id', 'Predecessor Project'),
        'successor_ids': fields.many2many('project.project', 'projects_relationships', 'predecessor_id', 'project_id', 'Successor Project'),                                                  
    }
    

     
    def set_restart(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'open'})        
        return True
    
    def set_reopen(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'open'})        
        return True
    
    #def set_open(self, cr, uid, ids, *args):
        
        # res = super(project,self).set_open(cr, uid, ids, *args)
        
        # for proj in self.browse(cr, uid, ids, context=None):
        #    analytic_account_id = proj.analytic_account_id.id
            
        # account_analytic_line_plan_obj=self.pool.get('account.analytic.line.plan')
        # account_analytic_line_plan_ids = account_analytic_line_plan_obj.search(cr, uid, [('account_id', '=', analytic_account_id)], context=None)
        
        # product_obj=self.pool.get('product.product')
        
        # purchase_order_obj=self.pool.get('purchase.order')
        # purchase_order_ids = purchase_order_obj.search(cr, uid, [('project_id', '=', proj.id),('state','<>','cancel')], context=None)

        #purchase_order_line_obj=self.pool.get('purchase.order.line')
        
                
        #for account_analytic_line_plan_id in account_analytic_line_plan_ids:
        #    account_analytic_line_plan=account_analytic_line_plan_obj.browse(cr, uid, account_analytic_line_plan_id, context=None)
        #    
        #    journal_type = account_analytic_line_plan.journal_id and account_analytic_line_plan.journal_id.type or False             
        #    
            #if account_analytic_line_plan.product_id:
            #    product=product_obj.browse(cr, uid, account_analytic_line_plan.product_id.id, context=None)
            #    if product.supply_method == 'buy' and journal_type == 'purchase':
            #        for purchase_order_id in purchase_order_ids:
            #            purchase_order_line_ids = purchase_order_line_obj.search(cr, uid, [('order_id', '=', purchase_order_id),('product_id','=',account_analytic_line_plan.product_id.id)], context=None)
            #        
            #        if not purchase_order_ids or not purchase_order_line_ids:
            #            raise osv.except_osv(_('User Error'),
            #            _('You cannot start the project.\n'\
            #              'The project contains a cost estimate for the product "%s" which has as supply method "buy".\n'\
            #              'You must create a purchase order linked to this project to procure this product.')
            #             % (product.name))      
             
        #return res
    
        
    def set_ready(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'ready'})
        self.send_ready(cr, uid, ids)
        return True
    
    
    def send_ready(self, cr, uid, ids):

        project_br = self.browse(cr,uid,ids)
        for p in project_br:
            
#            subject = _("'%s' is ready to start") % p.complete_wbs_name
            if p.user_id and p.user_id.address_id and p.user_id.address_id.email:
                to_adr = p.user_id.address_id.email
                #signature = p.user_id.signature
            else:
                raise osv.except_osv(_('Error'), _("Couldn't send mail because the project manager email address is not configured!"))
#
#            from_adr = tools.config.get('email_from', False) or p.user_id.address_id.email
#
#
#            
#            project_name = u'Project name: %s' %(tools.ustr(p.name))
#            user_id = u'Project manager: %s' %(tools.ustr(p.user_id.name)) 
#            complete_wbs_code = u'WBS code: %s' %(tools.ustr(p.complete_wbs_code)) 
#            complete_wbs_name = u'WBS path: %s' %(tools.ustr(p.complete_wbs_name)) 
#            
#            vals = [project_name, user_id, complete_wbs_code, complete_wbs_name]
#            
#            header = u'\n'.join(vals)
#            footer = ''
#            body = u'%s\n%s\n%s\n\n-- \n%s' % (header, p.description, footer, signature)
#            
#            mail_id = tools.email_send(from_adr, to_adr, subject, tools.ustr(body), email_bcc=[from_adr])
            
            email_template_ids = self.pool.get('email.template').search(cr,uid,[('object_name.name','=','Project'),('name','=','Project status change')],context=None)
            for email_template_id in email_template_ids:
                self.pool.get('email.template').generate_mail(cr,uid,email_template_id,ids,context=None)
                        
            #if not mail_id:
            #    raise osv.except_osv(_('Error'), _("Couldn't send mail! Check the email ids and smtp configuration settings"))
#            
#            msg_dict = {'new': 'Send', 'reply': 'Reply', 'forward': 'Forward'}
#            
#            self.history(cr, uid,[p], _(msg_dict['new']), history=True,email=to_adr, details=body,subject=subject, email_from=from_adr, message_id=None, references=None, attach=None)
            
        return {}    
    

    def set_done(self, cr, uid, ids, *args):
        
        res = super(project,self).set_done(cr, uid, ids, *args)
        
        project_obj=self.pool.get('project.project')
        projects=self.browse(cr, uid, ids, context=None)
        
        for p in projects:
            for successor in p.successor_ids:
                successor_project_br = project_obj.browse(cr, uid, successor.id, context=None)
                if successor_project_br.state == 'draft':
                    project_obj.set_ready(cr, uid, [successor.id])
                    
        for proj in projects:
            purchase_order_obj=self.pool.get('purchase.order')
            purchase_order_ids = purchase_order_obj.search(cr, uid, [('project_id', '=', proj.id),('state','not in',['cancel','done','approved'])], context=None)
            
            if purchase_order_ids:                    
                raise osv.except_osv(_('User Error'), _('You must complete all active purchase orders related to this project before closing it.'))
                            
        return res        

project()

