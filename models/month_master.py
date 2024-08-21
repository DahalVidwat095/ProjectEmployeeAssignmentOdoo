from odoo import models, fields

class MonthMaster(models.Model):
    _name = "month.master"
    _description = "Month Master"
    _rec_name = 'month'

    month = fields.Integer(required=True, help='Unique Key', index=True)
    order = fields.Integer(required=True, help='Unique Order')

    _sql_constraints = [
        ('unique_month', 'UNIQUE(month)', 'The month must be unique.'),
    ]
