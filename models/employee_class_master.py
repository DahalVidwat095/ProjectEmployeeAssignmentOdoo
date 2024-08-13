from odoo import models, fields

class EmployeeClassMaster(models.Model):
    _name = "employee.class.master"
    _description = "Employee Class Master"
    _rec_name = 'code'

    code = fields.Char(required=True, help='Unique Key', index=True)
    name = fields.Char(required=True)
    unit_price = fields.Float(required=True)
    delete_flag = fields.Boolean(default=False, help='False for available employee class and vice-versa.')
    description = fields.Text()

    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'The employee class code must be unique.'),
    ]