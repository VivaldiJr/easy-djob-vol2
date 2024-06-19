from odoo import http
from ..serializers.hr_candidate_course import HrCandidateCourseSerializer
from ..urls import hr_candidate_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request


class HrCandidateCourseController(http.Controller):
    @api_key_required()
    @http.route("{}/<int:candidate_id>/course".format(hr_candidate_endpoint), methods=["GET"], type="json", auth="none",
                csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.candidate.course']
        return DlinkHelper.JsonValidResponse(
            data=HrCandidateCourseSerializer(data=TABLE.sudo().search([("candidate_id", "=", kwargs.get("candidate_id", 0))]),
                                             many=True).serializer())

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key='course', type='int', relation="hr.course"),
        FieldRequired(key='start_date', type='datetime'),
        FieldRequired(key='end_date', type='datetime'),
        FieldRequired(key='description', type='str', required=False),

    ])
    @http.route("{}/<int:candidate_id>/course".format(hr_candidate_endpoint), methods=["POST"], type="json", auth="none",
                csrf=False, cors='*')
    def post(self, *args, **kwargs):
        args = request.httprequest.args
        course_id = kwargs.pop("course")
        kwargs.update({"course_name": course_id})
        TABLE = request.env['hr.candidate.course']
        candidate_course = TABLE.sudo().create(kwargs)
        return DlinkHelper.JsonValidResponse(data=HrCandidateCourseSerializer(data=candidate_course).serializer(), valid_code=201)

    @http.route("{}/<int:candidate_id>/course/<int:id>".format(hr_candidate_endpoint), methods=["DELETE"], type="json",
                auth="none",
                csrf=False, cors='*')
    def delete(self, *args, **kwargs):
        TABLE = request.env['hr.candidate.course']
        exist = TABLE.sudo().search([("id", "=", kwargs.get("id")), ("candidate_id", "=", kwargs.get("candidate_id"))])
        if not exist:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Object Not Found", error_code=404)
        exist.unlink()
        return DlinkHelper.JsonValidResponse(data={"detail": "OK"}, valid_code=200)
