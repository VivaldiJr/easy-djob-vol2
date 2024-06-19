import logging

from datetime import datetime, timedelta

from odoo import fields, models
from odoo.addons.dlink_api_utils import random_token
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from ..enviroment import EXPIRE_TOKEN
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class APIAccessToken(models.Model):
    _name = "dlink_auth_api.access_token"
    _description = _("API Access Token")
    user_id = fields.Many2one("res.users", string=_("User"), ondelete='cascade')

    device = fields.Char(string=_("Device ID"))

    token = fields.Char(string=_("Access Token"), required=True)
    refresh = fields.Char(string=_("Refresh Token"), required=True)

    token_expiry_date = fields.Datetime(string=_("Token Expiry Date"), required=True)
    refresh_expiry_date = fields.Datetime(string=_("Refresh Expiry Date"), required=True)

    scope = fields.Char(string=_("Scope"))

    def find_or_create_token(self, user_id=None, device=None, create=False):
        if not user_id:
            user_id = self.env.user.id

        access_token = self.env['dlink_auth_api.access_token'].sudo().search(
            [("user_id", "=", user_id), ("device", "=", device)], order="id DESC", limit=1)

        if access_token:
            access_token = access_token[0]
            if access_token.has_expired():
                access_token = None

        if not access_token and create:
            token_expiry_date = datetime.now() + timedelta(minutes=EXPIRE_TOKEN.get('token', 24 * 60))
            refresh_expiry_date = datetime.now() + timedelta(minutes=EXPIRE_TOKEN.get('refresh', 144 * 60))
            vals = {
                "user_id": user_id,
                "device": device,

                "token_expiry_date": token_expiry_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                "refresh_expiry_date": refresh_expiry_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),

                "token": random_token(prefix='access'),
                "refresh": random_token(prefix='refresh'),

                "scope": "userinfo",

            }
            access_token = self.env['dlink_auth_api.access_token'].sudo().create(vals)
        if not access_token:
            return None
        return access_token.token

    def is_valid(self, scopes=None):
        self.ensure_one()
        return not self.has_expired() and self._allow_scopes(scopes)

    def has_expired(self):
        if not EXPIRE_TOKEN.get('value', True):
            return False
        self.ensure_one()
        return datetime.now() > fields.Datetime.from_string(self.token_expiry_date)

    def has_refresh_expired(self):
        if not EXPIRE_TOKEN.get('value', True):
            return False
        self.ensure_one()
        return datetime.now() > fields.Datetime.from_string(self.refresh_expiry_date)

    def refresh_token(self):

        token_expiry_date = datetime.now() + timedelta(minutes=EXPIRE_TOKEN.get('token', 24 * 60))
        refresh_expiry_date = datetime.now() + timedelta(minutes=EXPIRE_TOKEN.get('refresh', 144 * 60))
        json = {
            "user_id": self.user_id,
            "device": self.device,
            "token_expiry_date": token_expiry_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            "refresh_expiry_date": refresh_expiry_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            "token": random_token(prefix='access{}'.format(self.device)),
            "refresh": random_token(prefix='refresh{}'.format(self.device), length=60),
            "scope": "userinfo",
        }
        self.write(json)
        return self

    def _allow_scopes(self, scopes):
        self.ensure_one()
        if not scopes:
            return True

        provided_scopes = set(self.scope.split())
        resource_scopes = set(scopes)

        return resource_scopes.issubset(provided_scopes)


class Users(models.Model):
    _inherit = "res.users"
    token_ids = fields.One2many('dlink_auth_api.access_token', "user_id", string=_("Access Tokens"))

    def last_device_id(self):
        last_token = self.token_ids.sudo().search([], order='create_date DESC', limit=1)
        if last_token:
            return last_token.device
        return None
