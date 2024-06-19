from odoo import http
from ..serializers.hr_job_position import HrJobPositionSerializer
from ..urls import hr_job_position_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request


class HrJobPositionController(http.Controller):
    @api_key_required()
    @http.route(hr_job_position_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.job_position']
        return DlinkHelper.JsonValidResponse(
            data=HrJobPositionSerializer(data=TABLE.sudo().search([("name", "ilike", args.get("q", ""))]),
                                         many=True).serializer())

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key='name', type='str')
    ])
    @http.route(hr_job_position_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.job_position']
        job_position = TABLE.sudo().search([("name", "=", kwargs.get("name", None))])
        if not job_position:
            job_position = TABLE.sudo().create(kwargs)
        return DlinkHelper.JsonValidResponse(data=HrJobPositionSerializer(data=job_position).serializer(), valid_code=201)
