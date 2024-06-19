from odoo.addons.dlink_api_utils import random_token
from odoo import api, fields, models
from odoo.tools.translate import _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class NtizuCompanyToken(models.Model):
    _name = "ntizu.company.request.token"
    _description = _("Token For Valid Email")
    email = fields.Char(string="Email of Represented")
    provider = fields.Char(string=_("Provider"))
    token = fields.Char(string=_('Valid Token'), required=True)
    token_expiry_date = fields.Datetime(string=_("Token Expiry Date"), required=True)

    @api.model
    def create(self, vals):

        try:
            vals['token'] = random_token(length=6, number=not vals.get('provider', None))
            vals['token_expiry_date'] = datetime.now() + timedelta(minutes=10)
            MAIL = self.env['mail.mail']
            mensaje_correo = MAIL.sudo().create({
                'email_from': 'soporte.dl97@gmail.com',
                'email_to': vals['email'],
                'subject': 'Your Token for complete register company',
                'body_html': '{}?token={}'.format(vals['provider'], vals['token']) if vals.get('provider', None) else vals['token']
            })
            mensaje_correo.send()
            return super(NtizuCompanyToken, self).create(vals)

        except Exception as e:
            raise ValidationError(str(e))

    def has_expired(self):
        self.ensure_one()
        return datetime.now() > fields.Datetime.from_string(self.token_expiry_date)
