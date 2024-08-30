from odoo import models, fields, api

class ProjectEmployeeAssignPerMonth(models.Model):
    _name = "project.employee.assign.per.month"
    _description = "Project Employee Assign Per Month"

    project_code = fields.Many2one("project.master", required=True, help='Unique Key', index=True, context={'show_name': True})
    employee_code = fields.Many2one("employee.master", required=True, help='Unique Key', index=True, context={'show_name': True})
    month_01 = fields.Float(string='01', compute='_compute_hours', inverse='_inverse_hours', default=0.0, store=True)
    month_02 = fields.Float(string='02', compute='_compute_hours', inverse='_inverse_hours', default=0.0, store=True)
    month_03 = fields.Float(string='03', compute='_compute_hours', inverse='_inverse_hours', default=0.0, store=True)
    month_04 = fields.Float(string='04', compute='_compute_hours', inverse='_inverse_hours', default=0.0, store=True)
    month_05 = fields.Float(string='05', compute='_compute_hours', inverse='_inverse_hours', default=0.0, store=True)
    month_06 = fields.Float(string='06', compute='_compute_hours', inverse='_inverse_hours', default=0.0, store=True)
    month_07 = fields.Float(string='07', compute='_compute_hours', inverse='_inverse_hours', default=0.0, store=True)
    month_08 = fields.Float(string='08', compute='_compute_hours', inverse='_inverse_hours', default=0.0, store=True)
    month_09 = fields.Float(string='09', compute='_compute_hours', inverse='_inverse_hours', default=0.0, store=True)
    month_10 = fields.Float(string='10', compute='_compute_hours', inverse='_inverse_hours', default=0.0, store=True)
    month_11 = fields.Float(string='11', compute='_compute_hours', inverse='_inverse_hours', default=0.0, store=True)
    month_12 = fields.Float(string='12', compute='_compute_hours', inverse='_inverse_hours', default=0.0, store=True)
    related_assignment_ids = fields.One2many(
        comodel_name='project.employee.assign',
        inverse_name='project_code',
        string='Related Assignments',
        compute='_compute_related_assignments'
    )

    _sql_constraints = [
        ('unique_project_employee', 'UNIQUE(project_code, employee_code)', 'The combination of project code and employee code must be unique.')
    ]

    @api.depends('project_code', 'employee_code', 'related_assignment_ids.op_hours_actual')
    def _compute_hours(self):
        for record in self:
            assignments = self.env['project.employee.assign'].search([
                ('project_code', '=', record.project_code.id),
                ('employee_code', '=', record.employee_code.id)
            ])

            assignment_map = {assignment.month.month: assignment.op_hours_actual for assignment in assignments}

            for month in range(1, 13):
                month_field = f'month_{month:02d}'
                
                current_value = getattr(record, month_field)

                if month in assignment_map:
                    setattr(record, month_field, assignment_map[month])
                else:
                    if current_value in (None, 0.0):
                        setattr(record, month_field, 0.0)

    @api.depends('month_01', 'month_02', 'month_03', 'month_04', 'month_05', 'month_06', 'month_07', 'month_08', 'month_09', 'month_10', 'month_11', 'month_12')
    def _inverse_hours(self):
        for record in self:
            for month in range(1, 13):
                month_field = f'month_{month:02d}'
                month_value = getattr(record, month_field)

                assignment = self.env['project.employee.assign'].search([
                    ('project_code', '=', record.project_code.id),
                    ('employee_code', '=', record.employee_code.id),
                    ('month.month', '=', month)
                ], limit=1)

                if assignment:
                    assignment.op_hours_actual = month_value
                else:
                    if month_value != 0.0:
                        default_year = self.env['year.master'].search([('default_flag', '=', True)], limit=1)
                        if not default_year:
                            raise ValueError("Default year is not set. Please ensure that a default year is marked in Year Master.")

                        self.env['project.employee.assign'].create({
                            'project_code': record.project_code.id,
                            'employee_code': record.employee_code.id,
                            'year': default_year.id,
                            'month': self.env['month.master'].search([('month', '=', month)], limit=1).id,
                            'op_hours_planned': month_value,
                            'op_hours_actual': month_value,
                        })

    @api.depends('project_code', 'employee_code')
    def _compute_related_assignments(self):
        for record in self:
            record.related_assignment_ids = self.env['project.employee.assign'].search([
                ('project_code', '=', record.project_code.id),
                ('employee_code', '=', record.employee_code.id)
            ])
    
    def action_view_employee_assignments_per_month(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Assignments for {self.employee_code.name}',
            'res_model': 'project.employee.assign.per.month',
            'view_mode': 'tree',
            'view_id': self.env.ref('project_employee_assignment_system.view_employee_assign_per_month_tree').id,
            'domain': [('employee_code', '=', self.employee_code.id)],
            'context': {'default_employee_code': self.employee_code.id},
        }
