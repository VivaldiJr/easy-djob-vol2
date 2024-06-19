from odoo import http
from ..serializers.hr_course import HrCourseSerializer
from ..urls import hr_course_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request


class HrCourseController(http.Controller):
    @api_key_required()
    @http.route(hr_course_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.course']
        return DlinkHelper.JsonValidResponse(
            data=HrCourseSerializer(data=TABLE.sudo().search([("name", "ilike", args.get("q", ""))]), many=True).serializer())

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key='name', type='str')
    ])
    @http.route(hr_course_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.course']
        course = TABLE.sudo().search([("name", "=", kwargs.get("name", None))])
        if not course:
            course = TABLE.sudo().create(kwargs)
        return DlinkHelper.JsonValidResponse(data=HrCourseSerializer(data=course).serializer(), valid_code=201)
