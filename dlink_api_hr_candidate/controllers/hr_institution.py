from odoo import http
from ..serializers.hr_institution import HrInstitutionSerializer
from ..urls import hr_institution_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request


class HrInstitutionController(http.Controller):
    @api_key_required()
    @http.route(hr_institution_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.institution']
        return DlinkHelper.JsonValidResponse(
            data=HrInstitutionSerializer(data=TABLE.sudo().search([("name", "ilike", args.get("q", ""))]),
                                         many=True).serializer())

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key='name', type='str')
    ])
    @http.route(hr_institution_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.institution']
        institution = TABLE.sudo().search([("name", "=", kwargs.get("name", None))])
        if not institution:
            institution = TABLE.sudo().create(kwargs)
        return DlinkHelper.JsonValidResponse(data=HrInstitutionSerializer(data=institution).serializer(), valid_code=201)
