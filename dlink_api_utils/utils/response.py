import datetime
import json
import logging
from odoo.exceptions import ValidationError

from odoo.http import Response
from typing import Optional, Dict, List

_logger = logging.getLogger(__name__)


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, bytes):
        return str(o)


class DlinkHelper:

    @staticmethod
    def JsonValidResponse(data: Dict or list, meta: Optional[Dict] = None, valid_code: Optional[int] = 200,
                          isHttp: Optional[bool] = False) -> Dict[str, any]:
        """
        Return a JsonResponse with the given data and status code if code is valid or no exceptions.
        """
        json_return = {"http_status": valid_code, 'data': data}
        if meta:
            json_return['meta'] = meta
        # Response.status = str(valid_code)
        if isHttp:
            return Response(
                mimetype='application/json',
                status=valid_code,
                content_type="application/json; charset=utf-8",
                response=json.dumps(data, default=default)
            )

        return json_return

    @staticmethod
    def JsonErrorResponse(error: ValidationError or List[Dict], error_code: Optional[int] = 400, error_message: Optional[str] = "", isHttp: Optional[bool] = False) -> \
            Dict[
                str, any]:
        """
        Return a JsonResponse with the given data and status code if code is not valid or with exceptions.
        """

        json_return = {"http_status": error_code, 'data': {
            "message": str(error).replace('\"', '') if type(error) == ValidationError else error_message,
            "errors": error if type(error) == list else []
        }}
        if isHttp:
            return Response(
                mimetype='application/json',
                status=error_code,
                content_type="application/json; charset=utf-8",
                response=json.dumps(json_return, default=default)
            )

        return json_return
