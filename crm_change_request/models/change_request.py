# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields


class LeadToChangeRequestWizard(osv.TransientModel):
    """
    wizard to convert a Lead into a Change Request and move the Mail Thread
    """
    _name = "crm.lead2cr.wizard"
    _inherit = 'crm.partner.binding'

    _columns = {
        "lead_id": fields.many2one(
            "crm.lead", "Lead", domain=[("type", "=", "lead")]
        ),
        "project_id": fields.many2one("project.project", "Project"),
        "change_category_id": fields.many2one(
            "change.management.category", "Change Category"
        ),
    }

    _defaults = {
        "lead_id": lambda self, cr, uid, context=None: context.get('active_id')
    }

    def action_lead_to_change_request(self, cr, uid, ids, context=None):
        # get the wizards and models
        wizards = self.browse(cr, uid, ids, context=context)
        Lead = self.pool["crm.lead"]
        CR = self.pool["change.management.change"]
        Attachment = self.pool['ir.attachment']

        for wizard in wizards:
            # get the lead to transform
            lead = wizard.lead_id

            partner = self._find_matching_partner(cr, uid, context=context)
            if not partner and (lead.partner_name or lead.contact_name):
                partner_ids = Lead.handle_partner_assignation(
                    cr, uid, [lead.id], context=context
                )
                partner = partner_ids[lead.id]

            # create new change request
            vals = {
                "description": lead.name,
                "description_event": lead.description,
                "email_from": lead.email_from,
                "project_id": wizard.project_id.id,
                "change_category_id": wizard.change_category_id.id
            }
            change_id = CR.create(cr, uid, vals, context=None)
            change = CR.browse(cr, uid, change_id, context=None)
            # move the mail thread
            Lead.message_change_thread(
                cr, uid, lead.id, change_id,
                "change.management.change", context=context
            )
            # Move attachments
            attachment_ids = Attachment.search(
                cr, uid,
                [('res_model', '=', 'crm.lead'), ('res_id', '=', lead.id)],
                context=context
            )
            Attachment.write(
                cr, uid, attachment_ids,
                {'res_model': 'change.management.change', 'res_id': change_id},
                context=context
            )
            # Archive the lead
            Lead.write(cr, uid, [lead.id], {'active': False}, context=context)
            # delete the lead
            # Lead.unlink(cr, uid, [lead.id], context=None)
        # return the action to go to the form view of the new CR
        view_id = self.pool.get('ir.ui.view').search(
            cr, uid,
            [
                ('model', '=', 'change.management.change'),
                ('name', '=', 'change_form_view')
            ]
        )
        return {
            'name': 'CR created',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'change.management.change',
            'type': 'ir.actions.act_window',
            'res_id': change_id,
            'context': context
        }
