from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
import string
import random
import hashlib


def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def generate_hash(prefix):
    now = datetime.now()
    date_string = now.strftime("%d/%m/%Y %H:%M:%S")
    hash_object = hashlib.sha256(date_string.encode())
    hash_string = hash_object.hexdigest()
    return "{}.{}".format(prefix, hash_string)


class ApiKey(models.Model):
    _name = 'dlink.api.util.apikey'
    _description = _('ApiKeys for access endpoints')

    name = fields.Char(string='Name')
    expire = fields.Datetime()
    revoke = fields.Boolean(default=False)
    prefix = fields.Char()
    hash = fields.Char()

    def has_revoque_or_expire(self):
        self.ensure_one()
        return self.revoke or (self.expire and datetime.now() > fields.Datetime.from_string(self.expire))

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            raise ValidationError(_('The field "Name" is required'))
        prefix = generate_random_string()
        hash = generate_hash(prefix)

        vals['prefix'] = prefix
        vals['hash'] = hash
        res = super(ApiKey, self).create(vals)

        warning_message = '{} {hash}'.format(_("Your ApiKey is"), hash=hash)

        # Mostrar un popUp con el hash
        # Agrega aquí cualquier otra funcionalidad que desees ejecutar al crear una nueva instancia de la clase ApiKey
        return res
