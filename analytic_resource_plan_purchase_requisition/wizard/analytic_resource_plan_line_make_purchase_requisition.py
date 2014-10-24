# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
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

from tools.translate import _
from openerp.osv import fields, osv, orm


class analytic_resouce_plan_line_make_purchase_requisition(orm.TransientModel):
    _name = "analytic.resource.plan.line.make.purchase.requisition"
    _description = "Resource plan make purchase requisition"

    def _get_requisition_lines(self, cr, uid, context=None):
        """
        Returns the order lines associated to the analytic accounts selected.
        """
        if context is None:
            context = {}

        record_ids = context and context.get('active_ids', False)

        if record_ids:
            requisition_line_ids = []
            line_plan_obj = self.pool.get('analytic.resource.plan.line')

            for line in line_plan_obj.browse(cr, uid, record_ids, context=context):
                    for requisition_line in line.requisition_line_ids:
                        requisition_line_id = requisition_line and requisition_line.id
                        requisition_line_ids.extend([requisition_line_id])
            if requisition_line_ids:
                return requisition_line_ids
        return False

    _columns = {
        'requisition_type': fields.selection([('exclusive',
                                               'Purchase Requisition (exclusive)'),
                                              ('multiple',
                                               'Multiple Requisitions')],
                                             'Requisition Type',
                                             required=True,
                                             help="Purchase Requisition (exclusive):  "
                                                  "On the confirmation of a purchase order, "
                                                  "it cancels the remaining purchase order.\n"
                                                  "Purchase Requisition(Multiple):  "
                                                  "It allows to have multiple purchase orders."
                                                  " On confirmation of a purchase order it does "
                                                  "not cancel the remaining orders"""),

        'date_end': fields.datetime('Requisition Deadline'),

        'requisition_line_ids': fields.many2many('purchase.requisition.line',
                                                 'make_purchase_requisition_line_rel',
                                                 'requisition_line_id',
                                                 'make_purchase_requisition_id'),
    }

    _defaults = {
        'requisition_line_ids': _get_requisition_lines,
    }

    def make_purchase_requisitions(self, cr, uid, ids, context=None):        
        """
             To make purchase requisitions

             @param self: The object pointer.
             @param cr: A database cursor
             @param uid: ID of the user currently logged in
             @param ids: the ID or list of IDs
             @param context: A standard dictionary

             @return: A dictionary which of fields with values.

        """

        if context is None:
            context = {}
        res = []
        make_requisition = self.browse(cr, uid, ids[0], context=context)            
        
        record_ids = context and context.get('active_ids', False)
        if record_ids:            
            line_plan_obj = self.pool.get('analytic.resource.plan.line')
            requisition_obj = self.pool.get('purchase.requisition')
            requisition_line_obj = self.pool.get('purchase.requisition.line')

            company_id = False
            purchase_id = False
            product_names = []

            for line in line_plan_obj.browse(cr, uid, record_ids, context=context):
                if line.product_id.name:
                    product_names.insert(0, line.product_id.name)    
                else:
                    product_names.insert(0, '')
                    
            requisition_name = ', '.join(product_names)
            for line in line_plan_obj.browse(cr, uid, record_ids, context=context):
                    uom_id = line.product_uom_id                                        
                    line_company_id = line.company_id and line.company_id.id or False  
                    if company_id is not False and line_company_id != company_id:
                        raise osv.except_osv(
                            _('Could not create purchase requisition !'),
                            _('You have to select lines from the same company.'))
                    else:
                        company_id = line_company_id        
                                                                        
                    purchase_requisition_line = {
                        'product_qty': line.unit_amount,
                        'product_id': line.product_id.id,
                        'product_uom_id': uom_id.id,
                    }
                    if purchase_id is False:
                        purchase_id = requisition_obj.create(cr, uid, {
                            'origin': '',
                            'exclusive': make_requisition.requisition_type,
                            'date_end': make_requisition.date_end,
                            'company_id': company_id,                            
                  
                        
                        }, context=context)
                                                        
                    purchase_requisition_line.update({'requisition_id': purchase_id,
                                                      'account_analytic_id': line.account_id and line.account_id.id, })
                    
                    requisition_line_id = requisition_line_obj.create(cr,
                                                                      uid,
                                                                      purchase_requisition_line,
                                                                      context=context)
                    values = {
                        'requisition_line_ids': [(4, requisition_line_id)]
                    }
                    line_plan_obj.write(cr, uid, [line.id], values, context=context)
                    res.append(requisition_line_id)

        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('Purchase requisition lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.requisition.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }        

analytic_resouce_plan_line_make_purchase_requisition()