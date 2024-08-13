from odoo import models, fields

class DepartmentMaster(models.Model):
    _name = "department.master"
    _description = "Department Master"
    _rec_name = 'code'

    code = fields.Char(required=True, help='Unique Key', index=True)
    name = fields.Char(required=True)
    order = fields.Integer(required=True)
    delete_flag = fields.Boolean(default=False, help='False for available department and vice-versa.')
    description = fields.Text()

    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'The department code must be unique.'),
    ]
