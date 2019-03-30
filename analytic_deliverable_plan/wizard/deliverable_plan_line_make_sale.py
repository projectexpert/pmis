# -*- coding: utf-8 -*-
#    Copyright 2018 LUXIM, Slovenia (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError


class DeliverablePlanLineMakeSale(models.TransientModel):
    _name = "deliverable.plan.line.make.sale"
    _description = "Analytic deliverable plan line make sale"

    @api.multi
    def default_partner(self):
        context = self.env.context
        case_id = context and context.get('active_ids', []) or []
        case_id = case_id and case_id[0] or False
        crm_id = self.env['crm.lead'].browse(case_id)
        return crm_id and crm_id.partner_id.id or ''

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        default=default_partner
    )

    update_quotation = fields.Boolean(
        string='Update existing quotation'
    )

    @api.multi
    def make_order(self):
        context = self.env.context
        case_id = context and context.get('active_ids', []) or []
        case_id = case_id and case_id[0] or False
        crm_id = self.env['crm.lead'].browse(case_id)

        if self.update_quotation and crm_id and crm_id.order_ids:
            for order in crm_id.order_ids:
                if order.order_line:
                    order.order_line.unlink()

        if crm_id and crm_id.account_id:
            partner = crm_id.partner_id
            sale_order = self.env['sale.order']
            pricelist = partner.property_product_pricelist.id
            partner_address = partner.address_get(
                [
                    'default',
                    'invoice',
                    'delivery',
                    'contact'
                ]
            )
            sale_order_values = {
                'partner_id': partner.id,
                'opportunity_id': crm_id.id,
                'partner_invoice_id': partner_address['invoice'],
                'partner_shipping_id': partner_address['delivery'],
                'date_order': fields.datetime.now(),
            }

            for deliverable in crm_id.account_id.deliverable_ids:
                sale_order_values.update({
                    'client_order_ref': (
                        deliverable.account_id.complete_wbs_name),
                    'origin': deliverable.account_id.complete_wbs_code,
                    'account_id': deliverable.account_id.id
                })
                if deliverable and crm_id.account_id.pricelist_id:
                    sale_order_values.update({
                        'pricelist_id': deliverable.pricelist_id.id
                    })
                else:
                    sale_order_values.update({
                        'pricelist_id': pricelist
                    })
            order_id = sale_order.create(sale_order_values)
            order_lines = self.prepare_sale_order_line(case_id, order_id.id)
            self.create_sale_order_line(order_lines)
            return {
                'domain': str([('id', 'in', [order_id.id])]),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'name': _('Quotation'),
                'res_id': order_id.id
            }
        if crm_id and crm_id.order_ids:
            return {
                'domain': str([('id', 'in', crm_id.order_ids.ids)]),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'name': _('Quotation'),
                'res_ids': crm_id.order_ids.ids
            }

    def prepare_sale_order_line(self, case_id, order_id):
        lines = []
        case = self.env['crm.lead'].browse(case_id)
        order_id = self.env['sale.order'].browse(order_id)
        linked_deliverables = (
                case.account_id and case.account_id.deliverable_ids or []
        )
        if not linked_deliverables:
            raise ValidationError(
                _("There is no available deliverable to "
                  "make sale order!")
            )
        for deliverable in linked_deliverables:
            if deliverable.state in 'draft':
                continue
            for deliverable_line in deliverable:
                vals = {
                    'order_id': order_id and order_id.id,
                    'product_id': deliverable_line.product_id.id,
                    'name': deliverable_line.name,
                    'product_uom_qty': deliverable_line.unit_amount,
                    'product_uom': deliverable_line.product_uom_id.id,
                    'price_unit': deliverable_line.price_unit,
                }
                lines.append(vals)
        return lines

    def create_sale_order_line(self, order_lines):
        saleorder_line_obj = self.env['sale.order.line']
        for line in order_lines:
            saleorder_line_obj.create(line)


# noinspection PyAttributeOutsideInit
class CrmLead(models.Model):
    _inherit = "crm.lead"

    # project_id = fields.Many2one(
    #     comodel_name='project.project',
    #     string='Project',
    #     ondelete='set null',
    # )
    resource_cost_total = fields.Float(
        compute='_compute_resource_cost_total',
        string='Total Revenue from deliverable'
    )
    account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Project Account',
        ondelete='set null',
    )

    @api.multi
    def _compute_resource_cost_total(self):
        self.ensure_one()
        self.resource_cost_total = sum(
            [deliverable.price_total for deliverable in
                self.account_id and self.account_id.deliverable_ids
                if deliverable.state not in 'draft'])

    @api.multi
    @api.onchange('account_id')
    def account_id_change(self):
        self.ensure_one()
        if self.account_id:
            self.partner_id = self.account_id.partner_id.id
