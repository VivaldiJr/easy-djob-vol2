import werkzeug
from werkzeug.exceptions import BadRequest

from .utils import *
from .decorators import *

from . import models
from . import controllers
import json
import logging
from odoo.http import Request, JsonRPCDispatcher
from odoo.tools import date_utils
from odoo.addons.dlink_api_utils.urls import URL_API_BASE

_logger = logging.getLogger(__name__)


def dispatch(self, endpoint, args):
    try:
        self.jsonrequest = self.request.get_json_data()
    except ValueError as exc:

        methods = ['OPTIONS', 'GET', 'DELETE']
        if str(self.request.httprequest.url).__contains__(URL_API_BASE) and (
                self.request.httprequest.method in methods):
            self.jsonrequest = {}
        else:
            raise BadRequest("Invalid JSON data xds") from exc

    self.request.params = dict(self.jsonrequest.get('params', {}), **args)
    ctx = self.request.params.pop('context', None)
    if ctx is not None and self.request.db:
        self.request.update_context(**ctx)

    if self.request.db:
        result = self.request.registry['ir.http']._dispatch(endpoint)
    else:
        result = endpoint(**self.request.params)
    return self._response(result)


def make_json_response(self, data, headers=None, cookies=None, status=200):
    data_result = data
    status_result = status
    if str(self.httprequest.url).__contains__(URL_API_BASE):
        data_result = data.get("result", data.get("error", {}))
        status_result = data_result.get("http_status", 500)
    data = json.dumps(data_result, ensure_ascii=False, default=date_utils.json_default)

    headers = werkzeug.datastructures.Headers(headers)
    headers['Content-Length'] = len(data)
    headers['Content-Type'] = 'application/json; charset=utf-8'
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Max-Age'] = '3600'
    headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    headers[
        'Access-Control-Allow-Headers'] = 'Origin, Content-Type, Authorization, Device-Id, Access-Control-Allow-Origin, Access, X-Requested-With'
    return self.make_response(data, headers.to_wsgi_list(), cookies, status_result)


setattr(Request, 'make_json_response', make_json_response)
setattr(JsonRPCDispatcher, 'dispatch', dispatch)
print("STARTED CONFIGURATION FROM DLINK_API_UTILS")
