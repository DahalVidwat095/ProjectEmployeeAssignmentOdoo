from odoo import models, fields

class ProjectMaster(models.Model):
    _name = "project.master"
    _description = "Project Master"

    code = fields.Char(required=True, help='Unique Key', index=True)
    name = fields.Char(required=True)
    order = fields.Integer(required=True)
    delete_flag = fields.Boolean(default=False, help='False for available project and vice-versa.')
    description = fields.Text()

    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'The project code must be unique.'),
    ]

    def _compute_display_name(self):
            for record in self:
                if self.env.context.get('show_name', False):
                     record.display_name = f"{record.name}"
                else:
                     record.display_name = f"{record.code}"
