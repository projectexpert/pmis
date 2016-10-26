# -*- coding: utf-8 -*-

def migrate(cr, version):
    """Update fields owner module to avoid Odoo deleting them on uninstall."""
    # pe_project_meetings
    cr.execute("""UPDATE ir_model_data
                  SET module='pe_project_meetings'
                  WHERE module='project_meetings'
                    AND name LIKE 'field_%'""")
