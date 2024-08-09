{
    'name': "Project Employee Assignment System",
    'depends': ['base'],
    'sequence': 2,
    'author': 'Creation Software and IT Solutions',
    'summary': 'Project Employee Assignment System for CSI Solutions',
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/project_master_views.xml',
        'views/employee_master_views.xml',
        'views/department_master_views.xml',
        'views/employee_class_master_views.xml',
        'views/year_master_views.xml',
        'views/month_master_views.xml',
        'views/project_employee_assignment_menus.xml',
    ],
}
