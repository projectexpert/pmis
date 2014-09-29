# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
import netsvc

class sale_order(osv.osv):
    
    _inherit = "sale.order"
    

    _columns = {
        'project': fields.many2one('project.project', 'Project', readonly=True, states={'draft': [('readonly', False)]}, help="The project related to a sales order."),
        'project_manager': fields.related('project', 'user_id', readonly=True, string='Project Manager', type='many2one', relation="res.users", store=True),
    }
    
sale_order()

class sale_order_line(osv.osv):
    
    _inherit = 'sale.order.line'
    
    _columns = {
        'order_project': fields.related('order_id', 'project', type='many2one', relation='project.project', store=True, string='Project'),
        'order_project_manager': fields.related('order_project', 'user_id', readonly=True, string='Project Manager', type='many2one', relation="res.users", store=True),
    }

    def invoice_line_create(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        def _get_line_qty(line):
            if (line.order_id.invoice_quantity=='order') or not line.procurement_id:
                if line.product_uos:
                    return line.product_uos_qty or 0.0
                return line.product_uom_qty
            else:
                return self.pool.get('procurement.order').quantity_get(cr, uid,
                        line.procurement_id.id, context=context)

        def _get_line_uom(line):
            if (line.order_id.invoice_quantity=='order') or not line.procurement_id:
                if line.product_uos:
                    return line.product_uos.id
                return line.product_uom.id
            else:
                return self.pool.get('procurement.order').uom_get(cr, uid,
                        line.procurement_id.id, context=context)

        create_ids = []
        sales = {}
        for line in self.browse(cr, uid, ids, context=context):
            if not line.invoiced:
                if line.product_id:
                    a = line.product_id.product_tmpl_id.property_account_income.id
                    if not a:
                        a = line.product_id.categ_id.property_account_income_categ.id
                    if not a:
                        raise osv.except_osv(_('Error !'),
                                _('There is no income account defined ' \
                                        'for this product: "%s" (id:%d)') % \
                                        (line.product_id.name, line.product_id.id,))
                else:
                    prop = self.pool.get('ir.property').get(cr, uid,
                            'property_account_income_categ', 'product.category',
                            context=context)
                    a = prop and prop.id or False
                uosqty = _get_line_qty(line)
                uos_id = _get_line_uom(line)
                pu = 0.0
                if uosqty:
                    pu = round(line.price_unit * line.product_uom_qty / uosqty,
                            self.pool.get('decimal.precision').precision_get(cr, uid, 'Sale Price'))
                fpos = line.order_id.fiscal_position or False
                a = self.pool.get('account.fiscal.position').map_account(cr, uid, fpos, a)
                if not a:
                    raise osv.except_osv(_('Error !'),
                                _('There is no income category account defined in default Properties for Product Category or Fiscal Position is not defined !'))
                inv_id = self.pool.get('account.invoice.line').create(cr, uid, {
                    'name': line.name,
                    'origin': line.order_id.name,
                    'account_id': a,
                    'price_unit': pu,
                    'quantity': uosqty,
                    'discount': line.discount,
                    'uos_id': uos_id,
                    'product_id': line.product_id.id or False,
                    'invoice_line_tax_id': [(6, 0, [x.id for x in line.tax_id])],
                    'note': line.notes,
                    'account_analytic_id': line.order_id.project and line.order_id.project.analytic_account_id and line.order_id.project.analytic_account_id.id or False,
                    
                })
                cr.execute('insert into sale_order_line_invoice_rel (order_line_id,invoice_id) values (%s,%s)', (line.id, inv_id))
                self.write(cr, uid, [line.id], {'invoiced': True})
                sales[line.order_id.id] = True
                create_ids.append(inv_id)
        # Trigger workflow events
        wf_service = netsvc.LocalService("workflow")
        for sid in sales.keys():
            wf_service.trg_write(uid, 'sale.order', sid, cr)
        return create_ids


sale_order_line()

class project(osv.osv):
    _inherit = "project.project"
    
    def _get_sale_project_id(self, cr, uid, ids, context=None):
        project_id = []
        for sale_order_obj in self.pool.get('sale.order').browse(cr,uid,ids,context=context):
            project_id.append(sale_order_obj.project.id)
        return project_id
    
    def _order_count(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for id in ids:
            order_ids = self.pool.get('sale.order').search(cr,uid,[('project.id','=',id)],context=context)
            order_count = order_ids and len(order_ids) or 0
            res[id] = order_count
        return res
    
    _columns = {
                'order_count': fields.function(_order_count, method=True, type='integer', string='Associated Sale Order(s)',
#                                               store={
#                                                     'sale.order' : (_get_sale_project_id, ['project'],5),
#                                                     }, help="Gives the number of sale order associated with the project"
                ),
                }
project()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
