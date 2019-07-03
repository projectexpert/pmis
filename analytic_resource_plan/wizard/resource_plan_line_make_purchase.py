#    Copyright 2019 LUXIM, Slovenia (Matjaž Mozetič)
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError


class ResourcePlanLineMakePurchase(models.TransientModel):
    _name = "resource.plan.line.make.purchase"
    _description = "Analytic resource plan line make purchase"

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
            purchase_order = self.env['purchase.order']
            # TODO: check vendor pricelist for purchases field name
            pricelist = partner.property_product_pricelist.id
            partner_address = partner.address_get(
                [
                    'default',
                    'invoice',
                    'delivery',
                    'contact'
                ]
            )
            purchase_order_values = {
                'partner_id': partner.id,
                'opportunity_id': crm_id.id,
                'partner_invoice_id': partner_address['invoice'],
                'partner_shipping_id': partner_address['delivery'],
                'date_order': fields.datetime.now(),
            }

            for resource in crm_id.account_id.resource_ids:
                purchase_order_values.update({
                    'client_order_ref': (
                        resource.account_id.name),
                    'origin': resource.account_id.code,
                    'account_id': resource.account_id.id
                })
                if resource:
                    purchase_order_values.update({
                        'pricelist_id': pricelist
                    })
                # if resource and crm_id.account_id.pricelist_id:
                #     purchase_order_values.update({
                #         'pricelist_id': resource.pricelist_id.id
                #     })
                # else:
                #     purchase_order_values.update({
                #         'pricelist_id': pricelist
                #     })
            order_id = purchase_order.create(purchase_order_values)
            order_lines = self.prepare_purchase_order_line(case_id, order_id.id)
            self.create_purchase_order_line(order_lines)
            return {
                'domain': str([('id', 'in', [order_id.id])]),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'purchase.order',
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
                'res_model': 'purchase.order',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'name': _('Quotation'),
                'res_ids': crm_id.order_ids.ids
            }

    def prepare_purchase_order_line(self, case_id, order_id):
        lines = []
        case = self.env['crm.lead'].browse(case_id)
        order_id = self.env['purchase.order'].browse(order_id)
        linked_resources = (
                case.account_id and case.account_id.resource_ids or []
        )
        if not linked_resources:
            raise ValidationError(
                _("There is no available resource to "
                  "make purchase order!")
            )
        for resource in linked_resources:
            if resource.state in 'draft':
                continue
            for resource_line in resource:
                vals = {
                    'order_id': order_id and order_id.id,
                    'product_id': resource_line.product_id.id,
                    'name': resource_line.name,
                    'product_qty': resource_line.unit_amount,
                    'product_uom': resource_line.product_uom_id.id,
                    'price_unit': resource_line.price_unit,
                    'date_planned': resource_line.date,
                    'account_analytic_id': resource_line.account_id.id,
                    'resource_id': self
                }
                lines.append(vals)
        return lines

    def create_purchase_order_line(self, order_lines):
        purchaseorder_line_obj = self.env['purchase.order.line']
        for line in order_lines:
            purchaseorder_line_obj.create(line)


# noinspection PyAttributeOutsideInit
class CrmLead(models.Model):
    _inherit = "crm.lead"

    # project_id = fields.Many2one(
    #     comodel_name='project.project',
    #     string='Project',
    #     ondelete='set null',
    # )
    planned_cost_total = fields.Float(
        compute='_compute_planned_cost_total',
        string='Total planned cost'
    )
    account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Project Account',
        ondelete='set null',
    )

    @api.multi
    def _compute_planned_cost_total(self):
        self.ensure_one()
        self.planned_cost_total = sum(
            [resource.price_total for resource in
                self.account_id and self.account_id.resource_ids
                if resource.state not in 'draft'])

    @api.multi
    @api.onchange('account_id')
    def account_id_change(self):
        self.ensure_one()
        if self.account_id:
            self.partner_id = self.account_id.partner_id.id
