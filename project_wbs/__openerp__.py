{
    'name': 'Work Breakdown Structure',
    'version': '2.0.6',
    'author':   'Eficent, '
                'Matmoz d.o.o.',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
    ],
    'website':  'http://www.eficent.com, '
                'http://www.matmoz.si',
    'category': 'Project Management',
    'depends':  [
        'project',
        'analytic',
        'project_issue',
        'account_analytic_analysis'
    ],
    'license': 'AGPL-3',
    'summary': 'Project Work Breakdown Structure',
    'description': """
Project Scope
- The hierarchy of a project is considered the WBS(Work Breakdown Structure)
- The analytic accounts in the project hierarchies are considered WBS
  components
- The analytic account code is shown in the project
- The complete WBS path code  is shown in the analytic account and in the
  project
- The complete WBS path name is shown in the analytic account and in the
  project
- The WBS paths are concatenated with /
- It is possible to search projects by complete WBS path code & name
- It is possible to search tasks by project complete WBS path code & name
- The WBS components can be classified as project, phase, deliverable, work
  package.
- The classification is shown in the project and analytic account views
- A project stage attribute is incorporated in the analytic account and
  displayed in the project and analytic account views.
    """,
    'data': [
        'view/analytic_account_stage_view.xml',
        'view/account_analytic_account_view.xml',
        'view/project_project_view.xml',
        'view/project_wbs_data.xml',
        'view/project_configuration.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [

    ],
    'test': [
    ],
    'installable': True,
    'application': True,
}
