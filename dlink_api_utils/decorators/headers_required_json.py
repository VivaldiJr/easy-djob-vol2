import logging

from ..utils import *
from odoo.http import request
from functools import wraps

_logger = logging.getLogger(__name__)
header_device = 'device-id'


def headers_required_json(headers, isHttp=False):
    def decorate(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            response = []
            for k in headers.keys():
                if not request.httprequest.headers.get(k, None):
                    response.append({"key": k, "data": headers.get(k, None)})
            if len(response) > 0:
                return DlinkHelper.JsonErrorResponse(response, error_code=401, isHttp=isHttp)
            return fn(*args, **kwargs)

        return wrapper

    return decorate
