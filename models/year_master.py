from odoo import models, fields

class YearMaster(models.Model):
    _name = "year.master"
    _description = "Year Master"

    year = fields.Integer(required=True, help='Unique Key', index=True)
    order = fields.Integer(required=True)
    default_flag = fields.Boolean(default=False, help='If true is set, this year is selected by default.')
    delete_flag = fields.Boolean(default=False, help='False for active year and vice-versa.')

    _sql_constraints = [
        ('unique_year', 'unique(year)', 'The year must be unique.'),
    ]
