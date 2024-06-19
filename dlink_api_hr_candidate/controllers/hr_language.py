from odoo import http
from ..serializers.hr_language import HrLanguageSerializer
from ..urls import hr_language_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request


class HrLanguageController(http.Controller):
    @api_key_required()
    @http.route(hr_language_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.language']
        return DlinkHelper.JsonValidResponse(
            data=HrLanguageSerializer(data=TABLE.sudo().search([("name", "ilike", args.get("q", ""))]), many=True).serializer())

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key="name", type='str')
    ])
    @http.route(hr_language_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.language']
        language = TABLE.sudo().search([("name", "=", kwargs.get("name", None))])
        if not language:
            language = TABLE.sudo().create(kwargs)
        return DlinkHelper.JsonValidResponse(data=HrLanguageSerializer(data=language).serializer())
