import logging
import functools
from odoo.addons.dlink_api_utils import *
from odoo.http import request

_logger = logging.getLogger(__name__)
header_authorization = 'authorization'


def token_required(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        TABLE_API_AUTH_TOKEN = request.env['dlink_auth_api.access_token']
        access_token = request.httprequest.headers.get(header_authorization)
        device_id = request.httprequest.headers.get(header_device)
        if not access_token:
            return DlinkHelper.JsonErrorResponse([{"key": header_authorization, "data": "missing header in request"}], error_code=403)
        if not device_id:
            return DlinkHelper.JsonErrorResponse([{"key": header_device, "data": "missing header in request"}], error_code=403)
        access_token_data = TABLE_API_AUTH_TOKEN.sudo().search([("token", "=", access_token), ("device", "=", device_id)], order="id DESC", limit=1)
        if len(access_token_data) == 0:
            return DlinkHelper.JsonErrorResponse([{"key": header_authorization, "data": "Token Not found"}, ], error_code=401)

        if access_token_data.has_expired():
            return DlinkHelper.JsonErrorResponse([{"key": header_authorization, "data": "Token Expired"}], error_message="Token Expired", error_code=401)

        if access_token_data.find_or_create_token(user_id=access_token_data.user_id.id, device=device_id) != access_token:
            return DlinkHelper.JsonErrorResponse([{"key": header_authorization, "data": "Token seems to have expired or invalid"}], error_code=401)
        request.authToken = access_token_data
        return func(self, *args, **kwargs)

    return wrap
