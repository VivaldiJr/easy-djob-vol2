# -*- coding: utf-8 -*-
from odoo import models, fields
import uuid


class CustomMessage(models.Model):
    _name = 'custom.message'
    _inherit = ['mail.alias.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Custom Message'

    body = fields.Text(string='Corpo', required=True)
    sender_id = fields.Many2one('res.users', string='Remetente', required=True)
    recipient_id = fields.Many2one('res.users', string='Destinatário', required=True)
    date_sent = fields.Datetime(string='Data de Envio', default=fields.Datetime.now)

    def _alias_get_creation_values(self):

        unique_alias_name = f"custom_message_alias_{uuid.uuid4().hex[:8]}"
        alias_model_id = self.env['ir.model'].sudo().search([('model', '=', self._name)], limit=1).id
        return {
            'alias_name': unique_alias_name,
            'alias_model_id': alias_model_id,
            'alias_contact': 'everyone',
            'alias_defaults': {'model': self._name},
        }

    def _alias_get_model_name(self):

        return 'custom.message'
