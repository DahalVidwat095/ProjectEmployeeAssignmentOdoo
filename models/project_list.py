from odoo import models, fields, api

class ProjectList(models.Model):
    _name = "project.list"
    _description = "Project List"

    project_code = fields.Many2one("project.master", required=True, help='Unique Key', index=True)
    project_name = fields.Char(related='project_code.name', store=True, readonly=False)

    _sql_constraints = [
        ('unique_project_code', 'UNIQUE(project_code)', 'The project code must be unique.')
    ]

    def action_view_project_assignments_per_month(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Assignments for {self.project_name}',
            'res_model': 'project.employee.assign.per.month',
            'view_mode': 'tree',
            'view_id': self.env.ref('project_employee_assignment_system.view_project_assign_per_month_tree').id,
            'domain': [('project_code', '=', self.project_code.id)],
            'context': {'default_project_code': self.project_code.id},
        }
