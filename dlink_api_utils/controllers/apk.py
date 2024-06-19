import base64
from datetime import datetime

from odoo import http
from .. import api_key_required, fields_required_json, FieldRequired
from ..serializers.apk import ApkUpdateSerializer
from ..urls import appUpdates_endpoint

from ..utils import DlinkHelper
from odoo.http import request


class UtilsHttpController(http.Controller):
    @api_key_required(isHttp=True)
    @http.route("{}/<package_name>/".format(appUpdates_endpoint), methods=["GET"], type="http", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        TABLE_APK_UPDATES = request.env['dlink.api.util.app.update']
        query_search = [("package_name", "=", kwargs.get("package_name", ""))]
        exist_app = TABLE_APK_UPDATES.sudo().search(query_search, order="datetime desc", limit=1)
        return DlinkHelper.JsonValidResponse(data=ApkUpdateSerializer(data=exist_app).serializer(), isHttp=True)

    @fields_required_json(fields=[
        FieldRequired(key="name", type='str'),
        FieldRequired(key="version", type='str'),
        FieldRequired(key="file", type='file'),
    ], isHttp=True)
    @http.route("{}/<package_name>/".format(appUpdates_endpoint), methods=["POST"], type="http", auth="none", csrf=False, cors='*')
    def post(self, **kwargs):

        TABLE_APK_UPDATES = request.env['dlink.api.util.app.update']

        file = kwargs.get('file', None)
        kwargs['datetime'] = datetime.now()

        try:
            attachment = file.read()
            encode = base64.encodebytes(attachment)
            kwargs['file'] = encode
            query_search = [("package_name", "=", kwargs.get("package_name", None))]
            exist_app = TABLE_APK_UPDATES.sudo().search(query_search, order="datetime desc")
            if len(exist_app) > 0:
                if len(exist_app) > 2:
                    for i in range(2, len(exist_app)):
                        exist_app[i].unlink()

                same_version = TABLE_APK_UPDATES.sudo().search([("version", "=", kwargs.get("version", "1.0.1")), ], limit=1, order="datetime desc")
                if len(same_version) > 0:
                    exist_app[0].write(kwargs)
                    app = exist_app[0]
                else:
                    app = TABLE_APK_UPDATES.sudo().create(kwargs)
            else:
                app = TABLE_APK_UPDATES.sudo().create(kwargs)
            return DlinkHelper.JsonValidResponse(data=ApkUpdateSerializer(data=app).serializer(), isHttp=True)
        except Exception as e:
            return DlinkHelper.JsonErrorResponse(error=e, isHttp=True)
