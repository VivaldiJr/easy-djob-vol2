from odoo import http
from ..serializers.hr_study_area import HrStudyAreaSerializer
from ..urls import hr_study_area_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request


class HrStudyAreaController(http.Controller):
    @api_key_required()
    @http.route(hr_study_area_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.study_area']
        return DlinkHelper.JsonValidResponse(
            data=HrStudyAreaSerializer(data=TABLE.sudo().search([("name", "ilike", args.get("q", ""))]),
                                       many=True).serializer())

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key="name", type='str')
    ])
    @http.route(hr_study_area_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.study_area']
        st = TABLE.sudo().search([("name", "=", kwargs.get("name", None))])
        if not st:
            kwargs.update({"score": 0})
            st = TABLE.sudo().create(kwargs)
        return DlinkHelper.JsonValidResponse(data=HrStudyAreaSerializer(data=st).serializer())
