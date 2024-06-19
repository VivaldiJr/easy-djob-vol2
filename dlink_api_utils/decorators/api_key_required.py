import logging

from ..utils import *
from odoo.http import request
from functools import wraps

_logger = logging.getLogger(__name__)
header_device = 'device-id'


def api_key_required(isHttp=False):
    def decorate(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            X_API_KEY_REQUIRED = request.env['ir.config_parameter'].sudo().get_param('dlink_api_utils.api_key_required')
            X_API_KEY_HEADER = request.env['ir.config_parameter'].sudo().get_param('dlink_api_utils.api_key_header')
            if not X_API_KEY_HEADER:
                X_API_KEY_HEADER = 'x-api-key'
            header_name = X_API_KEY_HEADER
            if X_API_KEY_REQUIRED:
                x_api_key = request.httprequest.headers.get(header_name, None)
                if not x_api_key:
                    return DlinkHelper.JsonErrorResponse([
                        {
                            "key": header_name,
                            "data": "{} is required ".format(header_name)
                        }
                    ], error_code=401, isHttp=isHttp)

                TABLE_API_KEY = request.env['dlink.api.util.apikey']
                query_search = [("hash", "=", x_api_key)]
                access_apikey_data = TABLE_API_KEY.sudo().search(query_search, order="id DESC", limit=1)

                if not access_apikey_data or access_apikey_data.has_revoque_or_expire():
                    return DlinkHelper.JsonErrorResponse([
                        {
                            "key": header_name,
                            "data": "{} is invalid ".format(header_name)
                        }
                    ], error_code=401, isHttp=isHttp)
            return fn(*args, **kwargs)

        return wrapper

    return decorate
