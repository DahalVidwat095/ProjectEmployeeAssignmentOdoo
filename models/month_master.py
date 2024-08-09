from odoo import models, fields

class MonthMaster(models.Model):
    _name = "month.master"
    _description = "Month Master"

    month = fields.Integer(required=True, help='Unique Key', index=True)
    order = fields.Integer(required=True, help='Unique Order')

    _sql_constraints = [
        ('unique_year', 'unique(year)', 'The year must be unique.'),
        ('unique_order', 'unique(order)', 'The order must be unique.'),
    ]
