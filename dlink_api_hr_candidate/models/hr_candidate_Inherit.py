from odoo import models, fields


class HrDepartmentInherit(models.Model):
    _inherit = 'hr.department'

    website = fields.Char(string='Website')
    location = fields.Char(string='Location')
    description = fields.Text(string='Description')
