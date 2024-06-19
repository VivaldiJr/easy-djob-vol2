from odoo import http
from ..serializers.hr_company import HrCompanySerializer
from ..urls import hr_company_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request


class HrCompanyController(http.Controller):
    @api_key_required()
    @http.route(hr_company_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.company']
        return DlinkHelper.JsonValidResponse(data=HrCompanySerializer(data=TABLE.sudo().search([("name", "ilike", args.get("q", None))]), many=True).serializer())

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key='name', type='str')
    ])
    @http.route(hr_company_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.company']
        company = TABLE.sudo().search([("name", "=", kwargs.get("name", None))])
        if not company:
            company = TABLE.sudo().create(kwargs)
        return DlinkHelper.JsonValidResponse(data=HrCompanySerializer(data=company).serializer(), valid_code=201)
