# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']
    api_key_required = fields.Boolean(default=False, string="Api Key Required", config_parameter='dlink_api_utils.api_key_required')
    api_key_header = fields.Char(string="Api Key Header", config_parameter='dlink_api_utils.api_key_header', default='x-api-key')
