from odoo import models, fields, api

class ProjectAssignPerMonth(models.Model):
    _name = "project.assign.per.month"
    _description = "Project Assign Per Month"

    project_code = fields.Many2one("project.master", required=True, help='Unique Key', index=True)
    employee_code = fields.Many2one("employee.master", required=True, help='Unique Key', index=True)
    month_01 = fields.Float(string='01', compute='_compute_hours', default=0.0)
    month_02 = fields.Float(string='02', compute='_compute_hours', default=0.0)
    month_03 = fields.Float(string='03', compute='_compute_hours', default=0.0)
    month_04 = fields.Float(string='04', compute='_compute_hours', default=0.0)
    month_05 = fields.Float(string='05', compute='_compute_hours', default=0.0)
    month_06 = fields.Float(string='06', compute='_compute_hours', default=0.0)
    month_07 = fields.Float(string='07', compute='_compute_hours', default=0.0)
    month_08 = fields.Float(string='08', compute='_compute_hours', default=0.0)
    month_09 = fields.Float(string='09', compute='_compute_hours', default=0.0)
    month_10 = fields.Float(string='10', compute='_compute_hours', default=0.0)
    month_11 = fields.Float(string='11', compute='_compute_hours', default=0.0)
    month_12 = fields.Float(string='12', compute='_compute_hours', default=0.0)

    _sql_constraints = [
        ('unique_project_employee', 'UNIQUE(project_code, employee_code)', 'The combination of project code and employee code must be unique.')
    ]

    @api.depends('project_code', 'employee_code')
    def _compute_hours(self):
        for record in self:
            for month in range(1, 13):
                setattr(record, f'month_{month:02d}', 0.0)
                
            assignments = self.env['project.employee.assign'].search([
                ('project_code', '=', record.project_code.code),
                ('employee_code', '=', record.employee_code.code)
            ])
            
            for assignment in assignments:
                month_field = f'month_{assignment.month.month:02d}'
                if hasattr(record, month_field):
                    setattr(record, month_field, assignment.op_hours_actual)
