# -*- coding: utf-8 -*-

def migrate(cr, version):
    """Update fields owner module to avoid Odoo deleting them on uninstall."""
    # pe_project_task_issues
    cr.execute("""UPDATE ir_model_data
                  SET module='pe_project_task_issues'
                  WHERE module='project_task_issues'
                    AND name LIKE 'field_%'""")
