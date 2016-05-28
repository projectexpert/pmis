# coding: utf-8

from openerp.osv import fields, osv


class ConvertNoteChange(osv.TransientModel):

    """Convert Note to Task Wizard"""

    _name = 'convert.note.change'

    _columns = {
        # "note_id": fields.many2one(
        #     "note.note", "Note"
        # ),
        "change_category_id": fields.many2one(
            "change.management.category", "Change Category", required=True
        ),
        "project_id": fields.many2one(
            'project.project', 'Project', help='Project Linked', required=True
        ),
    }

    # _defaults = {
    #     "note_id": lambda self, cr, uid, context=None: context.get('active_id')
    # }

    def create_change(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids, context=context)
        change_obj = self.pool('change.management.change')
        note_obj = self.pool('note.note')
        note_brw = note_obj.browse(
            cr, uid, [context.get('active_id')], context=context)
        Attachment = self.pool['ir.attachment']

        # for wizard in wizards:
        #     # get the note to transform
        #     note_obj = wizard.note_id

        vals = {
            'description': note_brw[0].name,
            'description_event': note_brw[0].memo,
            'project_id': wizard.project_id.id,
            'user_id': uid,
            "change_category_id": wizard.change_category_id.id
        }

        change_id = change_obj.create(cr, uid, vals, context=context)

        # move the mail thread

        # note_obj.message_change_thread(
        #     cr, uid, note_obj.id, change_id,
        #     "change.management.change", context=context
        # )
        #
        # # Move attachments
        #
        # attachment_ids = Attachment.search(
        #     cr, uid,
        #     [('res_model', '=', 'note.note'), ('res_id', '=', note_obj.id)],
        #     context=context
        # )
        # Attachment.write(
        #     cr, uid, attachment_ids,
        #     {'res_model': 'change.management.change', 'res_id': change_id},
        #     context=context
        # )

        # Archive the note
        note_obj.write(cr, uid, [context.get('active_id')], {
            'open': False,
        })
        obj_model = self.pool.get('ir.model.data')

        # return the action to go to the form view of the new CR
        model_data_ids = obj_model.search(
            cr, uid, [
                ('model', '=', 'ir.ui.view'),
                ('name', '=', 'change_form_view')
            ]
        )
        resource_id = obj_model.read(
            cr, uid, model_data_ids,
            fields=['res_id']
        )[0]['res_id']

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'change.management.change',
            'views': [(resource_id, 'form')],
            'res_id': change_id,
            'type': 'ir.actions.act_window',
            'context': {},
        }
