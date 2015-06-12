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
    
    def set_ready(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'ready'})
        self.send_ready(cr, uid, ids)
        return True
    
    
    def send_ready(self, cr, uid, ids):

        project_br = self.browse(cr,uid,ids)
        for p in project_br:
            
            if p.user_id and p.user_id.address_id and p.user_id.address_id.email:
                to_adr = p.user_id.address_id.email
            else:
                raise osv.except_osv(_('Error'), _("Couldn't send mail because the project manager email address is not configured!"))
            
            email_template_ids = self.pool.get('email.template').search(cr,uid,[('object_name.name','=','Project'),('name','=','Project status change')],context=None)
            for email_template_id in email_template_ids:
                self.pool.get('email.template').generate_mail(cr,uid,email_template_id,ids,context=None)
                        
            
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

