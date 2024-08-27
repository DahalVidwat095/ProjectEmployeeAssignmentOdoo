from odoo import models, fields, api
from odoo.exceptions import ValidationError

class YearMaster(models.Model):
    _name = "year.master"
    _description = "Year Master"
    _rec_name = 'year'

    year = fields.Char(required=True, help='Unique Key', index=True)
    order = fields.Integer(required=True)
    default_flag = fields.Boolean(default=False, help='If true is set, this year is selected by default.')
    delete_flag = fields.Boolean(default=False, help='False for active year and vice-versa.')

    _sql_constraints = [
        ('unique_year', 'UNIQUE(year)', 'The year must be unique.'),
    ]

    @api.constrains('default_flag')
    def _check_only_one_default_year(self):
        if self.default_flag:
            existing_default = self.search([('default_flag', '=', True), ('id', '!=', self.id)])
            if existing_default:
                raise ValidationError("There can only be one default year.")
