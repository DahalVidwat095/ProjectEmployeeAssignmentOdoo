from odoo import models, fields

class ProjectEmployeeAssign(models.Model):
    _name = "project.employee.assign"
    _description = "Project Employee Assign "

    project_code = fields.Many2one("project.master", required=True, help='Unique Key', index=True, context={'show_name': True})
    employee_code = fields.Many2one("employee.master", required=True, help='Unique ', index=True)
    year = fields.Many2one("year.master", required=True, help='Unique Key', index=True)
    month = fields.Many2one("month.master", required=True, help='Unique Key', index=True)
    op_hours_planned = fields.Float(required=True)
    op_hours_actual = fields.Float(required=True)


    _sql_constraints = [
        ('unique_project_employee_year_month', 'UNIQUE(project_code, employee_code, year, month)', 'The combination of project code, employee code, year, and month must be unique.')
    ]
