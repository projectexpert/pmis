# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields


class IssuePartnerBinding(osv.osv_memory):
    """
    Handle the partner binding or generation in any issue wizard that requires
    such feature, like the issue2crm wizard. Try to find a matching partner
    from the issue model's information (name, email, phone number, etc) or
    create a new one on the fly.
    Use it like a mixin with the wizard of your choice.
    """
    _name = 'issue.partner.binding'
    _description = 'Handle partner binding or generation in Issue wizards.'
    _columns = {
        'action': fields.selection([
                ('exist', 'Link to an existing customer'),
                ('create', 'Create a new customer'),
                ('nothing', 'Do not link to a customer')
            ], 'Related Customer', required=True),
        'partner_id': fields.many2one('res.partner', 'Customer'),
    }

    def _find_matching_partner(self, cr, uid, context=None):
        """
        Try to find a matching partner regarding the active model data, like
        the customer's name, email, phone number, etc.

        :return int partner_id if any, False otherwise
        """
        if context is None:
            context = {}
        partner_id = False
        partner_obj = self.pool.get('res.partner')

        # The active model has to be a lead or a phonecall
        if (
            (context.get('active_model') == 'project.issue') and
            context.get('active_id')
        ):
            active_model = self.pool.get('project.issue').browse(
                cr, uid, context.get('active_id'), context=context
            )

        # Find the best matching partner for the active model
        if active_model:
            partner_obj = self.pool.get('res.partner')

            # A partner is set already
            if active_model.partner_id:
                partner_id = active_model.partner_id.id
            # Search through the existing partners based on the lead's email
            elif active_model.email_from:
                partner_ids = partner_obj.search(
                    cr, uid,
                    [('email', '=', active_model.email_from)],
                    context=context
                )
                if partner_ids:
                    partner_id = partner_ids[0]
            # Search through the existing partners based on the lead's partner
            # or contact name
            elif active_model.partner_name:
                partner_ids = partner_obj.search(
                    cr, uid,
                    [('name', 'ilike', '%'+active_model.partner_name+'%')],
                    context=context
                )
                if partner_ids:
                    partner_id = partner_ids[0]
            elif active_model.contact_name:
                partner_ids = partner_obj.search(
                    cr, uid, [
                        ('name', 'ilike', '%'+active_model.contact_name+'%')
                    ], context=context
                )
                if partner_ids:
                    partner_id = partner_ids[0]

        return partner_id

    def default_get(self, cr, uid, fields, context=None):
        res = super(IssuePartnerBinding, self).default_get(
            cr, uid, fields, context=context
        )
        partner_id = self._find_matching_partner(cr, uid, context=context)

        if 'action' in fields and not res.get('action'):
            res['action'] = partner_id and 'exist' or 'create'
        if 'partner_id' in fields:
            res['partner_id'] = partner_id

        return res


class Issue2ChangeWizard(osv.TransientModel):
    """
    wizard to convert an Issue into a Change Request and move the Mail Thread
    """
    _name = "project.issue2cr.wizard"
    _inherit = 'issue.partner.binding'

    _columns = {
        "issue_id": fields.many2one(
            "project.issue", "Issue"
        ),
        # "project_id": fields.many2one("project.project", "Project"),
        "change_category_id": fields.many2one(
            "change.management.category", "Change Category"
        ),
    }

    _defaults = {
        "issue_id": lambda self, cr, uid, context=None: context.get(
            'active_id')
    }

    def action_issue_to_change_request(self, cr, uid, ids, context=None):
        # get the wizards and models
        wizards = self.browse(cr, uid, ids, context=context)
        issue_obj = self.pool["project.issue"]
        cr_obj = self.pool["change.management.change"]
        attachment_obj = self.pool['ir.attachment']

        for wizard in wizards:
            # get the issue to transform
            issue = wizard.issue_id

            partner = self._find_matching_partner(cr, uid, context=context)
            if not partner and (issue.partner_name or issue.contact_name):
                partner_ids = issue_obj.handle_partner_assignation(
                    cr, uid, [issue.id], context=context
                )
                partner = partner_ids[issue.id]

            # create new change request
            vals = {
                "description": issue.name,
                "description_event": issue.description,
                "email_from": issue.email_from,
                "project_id": issue.project_id.id,
                "stakeholder_id": partner,
                "author_id": uid,
                "change_category_id": wizard.change_category_id.id
            }
            change_id = cr_obj.create(cr, uid, vals, context=None)
            change = cr_obj.browse(cr, uid, change_id, context=None)
            # move the mail thread
            issue_obj.message_change_thread(
                cr, uid, issue.id, change_id,
                "change.management.change", context=context
            )
            # Move attachments
            attachment_ids = attachment_obj.search(
                cr, uid,
                [
                    ('res_model', '=', 'project.issue'),
                    ('res_id', '=', issue.id)
                ],
                context=context
            )
            attachment_obj.write(
                cr, uid, attachment_ids,
                {'res_model': 'change.management.change', 'res_id': change_id},
                context=context
            )
            # Archive the lead
            issue_obj.write(
                cr, uid, [issue.id], {'active': False}, context=context
            )
            # delete the lead
            # issue_obj.unlink(cr, uid, [issue.id], context=None)
        # return the action to go to the form view of the new Issue
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
