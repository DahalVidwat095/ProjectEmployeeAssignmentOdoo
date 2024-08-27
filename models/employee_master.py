from odoo import models, fields

class EmployeeMaster(models.Model):
    _name = "employee.master"
    _description = "Employee Master"

    code = fields.Char(required=True, help='Unique Key', index=True)
    name = fields.Char(required=True)
    department_code = fields.Many2one('department.master', required=True, help='Enter Department Code.', index=True)
    class_code = fields.Many2one('employee.class.master', string='Employee Class Code', required=True, help='Enter Employee Class Code.', index=True)
    delete_flag = fields.Boolean(default=False, help='False for available employee and vice-versa.')
    description = fields.Text()

    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'The employee code must be unique.'),
    ]

    def _compute_display_name(self):
            for record in self:
                if self.env.context.get('show_name', False):
                     record.display_name = f"{record.name}"
                else:
                     record.display_name = f"{record.code}"
