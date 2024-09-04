from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class ProjectList(models.Model):
    _name = "project.list"
    _description = "Project List"

    project_code = fields.Many2one("project.master", required=True, help='Unique Key', index=True)
    project_name = fields.Char(related='project_code.name', store=True, readonly=False)
    employee_assignment_id = fields.Many2many('project.employee.assign', string='Employee Assignment')
    op_hours_planned = fields.Float(string='OP Hours Planned', compute='_compute_op_hours', store=True)
    op_hours_actual = fields.Float(string='OP Hours Actual', compute='_compute_op_hours', store=True)
    planned_cost = fields.Float(string='Planned Cost', compute='_compute_costs', store=True)
    actual_cost = fields.Float(string='Actual Cost', compute='_compute_costs', store=True)

    _sql_constraints = [
        ('unique_project_code', 'UNIQUE(project_code)', 'The project code must be unique.')
    ]

    @api.depends('project_code', 'employee_assignment_id')
    def _compute_op_hours(self):
        for record in self:
            assignments = self.env['project.list.per.month'].search([
                ('project_code', '=', record.project_code.id)
            ])
            _logger.info(f"Assignments: {assignments}")
            record.op_hours_planned = sum(assignments.mapped('op_hours_planned'))
            record.op_hours_actual = sum(assignments.mapped('op_hours_actual'))

    @api.depends('project_code')
    def _compute_costs(self):
        for record in self:
            monthly_records = self.env['project.list.per.month'].search([
                ('project_code', '=', record.project_code.id)
            ])
            _logger.info(f"Monthly Records: {monthly_records}")
            record.planned_cost = sum(monthly_records.mapped('planned_cost'))
            record.actual_cost = sum(monthly_records.mapped('actual_cost'))

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

    def action_view_project_list_per_month(self):
        self.ensure_one()

        assignments = self.env['project.employee.assign'].search([
            ('project_code', '=', self.project_code.id)
        ])

        assignments_by_month = {}
        for assignment in assignments:
            month_key = (assignment.year.id, assignment.month.id)
            if month_key not in assignments_by_month:
                assignments_by_month[month_key] = self.env['project.employee.assign']
            assignments_by_month[month_key] |= assignment

        for (year_id, month_id), month_assignments in assignments_by_month.items():
            total_op_hours_actual = sum(month_assignments.mapped('op_hours_actual'))

            values = {
                'project_code': self.project_code.id,
                'month': month_id,
                'employee_assignment_id': [(6, 0, month_assignments.ids)],
                'op_hours_actual': total_op_hours_actual,
            }

            existing_record = self.env['project.list.per.month'].search([
                ('project_code', '=', self.project_code.id),
                ('month', '=', month_id)
            ])

            if existing_record:
                existing_record.write(values)
            else:
                self.env['project.list.per.month'].create(values)

        return {
            'name': f'{self.project_name}',
            'type': 'ir.actions.act_window',
            'res_model': 'project.list.per.month',
            'view_mode': 'tree,form',
            'domain': [('project_code', '=', self.project_code.id)],
            'target': 'current',
        }

# class ProjectEmployeeAssign(models.Model):
#     _inherit = 'project.employee.assign'

#     @api.model
#     def create(self, vals):
#         res = super(ProjectEmployeeAssign, self).create(vals)
#         self._update_project_list(res)
#         return res

#     def write(self, vals):
#         res = super(ProjectEmployeeAssign, self).write(vals)
#         self._update_project_list(self)
#         return res

#     def unlink(self):
#         projects = self.mapped('project_code')
#         res = super(ProjectEmployeeAssign, self).unlink()
#         self._update_project_list(projects)
#         return res

#     @api.model
#     def _update_project_list(self, records):
#         if isinstance(records, models.Model):
#             projects = records.mapped('project_code')
#         else:
#             projects = records

#         if projects:
#             project_list = self.env['project.list'].search([('project_code', 'in', projects.ids)])
#             if project_list:
#                 project_list._compute_op_hours()
