from functools import wraps

from ..utils.response import DlinkHelper
from odoo.http import request
from .extra import *


def fields_required_json(fields: [FieldRequired], decline: [str] or None = None, isHttp=False):
    def decorate(fn):
        @wraps(fn)
        def wrapper(*args, **data):
            remove_fields = decline if decline else []

            if request.httprequest.method == 'GET':
                return fn(*args, **data)

            if not isHttp:
                data.update(request.get_json_data())
            data.update(request.httprequest.files)

            response = []
            for rf in remove_fields:
                if data.get(rf):
                    del data[rf]

            for f in fields:
                response = [*response, *f.validate(data, isHttp=isHttp)]
            if len(response) > 0:
                return DlinkHelper.JsonErrorResponse(response, error_code=400, isHttp=isHttp)
            return fn(*args, **data)

        return wrapper

    return decorate
