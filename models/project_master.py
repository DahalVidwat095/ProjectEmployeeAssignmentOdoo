from odoo import models, fields

class ProjectMaster(models.Model):
    _name = "project.master"
    _description = "Project Master"
    _rec_name = 'code'

    code = fields.Char(required=True, help='Unique Key', index=True)
    name = fields.Char(required=True)
    order = fields.Integer(required=True)
    delete_flag = fields.Boolean(default=False, help='False for available project and vice-versa.')
    description = fields.Text()

    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'The project code must be unique.'),
    ]
