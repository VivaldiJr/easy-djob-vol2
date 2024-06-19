from odoo import models, fields


class HrDepartmentInherit(models.Model):
    _inherit = 'hr.job'

    work_process = fields.Char(string='Work Process')
    address = fields.Char(string='Address')
    contract_detail = fields.Text(string='Contract Detail')
    min_salary = fields.Float(string='Minimum Salary')
    max_salary = fields.Float(string='Maximum Salary')
    currency_id = fields.Many2one('res.currency', string='Currency')
    select_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ], string='Select Frequency')
