from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class ProjectListPerMonth(models.Model):
    _name = 'project.list.per.month'
    _description = 'Project List Per Month'

    project_code = fields.Many2one('project.master', string='Project Code', help='Reference to the Project Master')
    month = fields.Many2one("month.master", required=True, help='Unique Key', index=True)
    employee_assignment_id = fields.Many2many('project.employee.assign', string='Employee Assignment')

    op_hours_planned = fields.Float(string='OP Hours Planned', compute='_compute_hours', store=True)
    op_hours_actual = fields.Float(string='OP Hours Actual', compute='_compute_hours', store=True)
    planned_cost = fields.Float(string='Planned Cost', compute='_compute_costs', store=True)
    actual_cost = fields.Float(string='Actual Cost', compute='_compute_costs', store=True)

    @api.depends('employee_assignment_id')
    def _compute_hours(self):
        for record in self:
            total_planned_hours = sum(record.employee_assignment_id.mapped('op_hours_planned'))
            total_actual_hours = sum(record.employee_assignment_id.mapped('op_hours_actual'))

            record.op_hours_planned = total_planned_hours
            record.op_hours_actual = total_actual_hours

    @api.depends('project_code', 'month')
    def _compute_costs(self):
        for record in self:
            employee_records = self.env['project.list.per.month.employee'].search([
                ('project_code', '=', record.project_code.id),
                ('month', '=', record.month.id)
            ])
            _logger.info(f"Records: {employee_records}")
            record.planned_cost = sum(employee_records.mapped('planned_cost'))
            record.actual_cost = sum(employee_records.mapped('actual_cost'))

    def action_view_project_list_per_month_employee(self):
        self.ensure_one()
        assignments = self.env['project.employee.assign'].search([
            ('project_code', '=', self.project_code.id),
            ('month', '=', self.month.id)
        ])
        self.env['project.list.per.month.employee'].search([
            ('project_code', '=', self.project_code.id),
            ('month', '=', self.month.id)
        ]).unlink()

        employee_list = []

        for assignment in assignments:
            employee_list.append({
                'project_code': self.project_code.id,
                'month': self.month.id,
                'employee_code': assignment.employee_code.id,
                'employee_assignment_id': assignment.id,
                'op_hours_planned': assignment.op_hours_planned,
                'op_hours_actual': assignment.op_hours_actual,
            })

        if employee_list:
            self.env['project.list.per.month.employee'].create(employee_list)

        return {
            'name': '%s(%s)' % (self.project_code.name, self.month.month),
            'type': 'ir.actions.act_window',
            'res_model': 'project.list.per.month.employee',
            'view_mode': 'tree',
            'domain': [('project_code', '=', self.project_code.id), ('month', '=', self.month.id)],
            'target': 'current',
        }
