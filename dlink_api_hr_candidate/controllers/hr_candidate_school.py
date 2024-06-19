from odoo import http
from ..serializers.hr_candidate_school import HrCandidateSchoolSerializer
from ..urls import hr_candidate_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request


class HrCandidateLanguageController(http.Controller):
    @api_key_required()
    @http.route("{}/<int:candidate_id>/school".format(hr_candidate_endpoint), methods=["GET"], type="json", auth="none",
                csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.candidate.school']
        return DlinkHelper.JsonValidResponse(
            data=HrCandidateSchoolSerializer(data=TABLE.sudo().search([("candidate_id", "=", kwargs.get("candidate_id", 0))]),
                                             many=True).serializer())

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key='start_date', type='datetime'),
        FieldRequired(key='end_date', type='datetime'),
        FieldRequired(key='study_area', type='int', relation='hr.study_area'),
        FieldRequired(key='institution', type='int', relation='hr.institution'),
        FieldRequired(key='description', type='str', required=False),
        FieldRequired(key='level_attained', type='str', choices=['no_degree', 'diploma', 'bachelor', 'master', 'doctorate']),
    ])
    @http.route("{}/<int:candidate_id>/school".format(hr_candidate_endpoint), methods=["POST"], type="json", auth="none",
                csrf=False, cors='*')
    def post(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.candidate.school']
        candidate_school = TABLE.sudo().create(kwargs)
        print(candidate_school)
        return DlinkHelper.JsonValidResponse(data=HrCandidateSchoolSerializer(data=candidate_school).serializer(), valid_code=201)

    @http.route("{}/<int:candidate_id>/school/<int:id>".format(hr_candidate_endpoint), methods=["DELETE"], type="json",
                auth="none",
                csrf=False, cors='*')
    def delete(self, *args, **kwargs):
        TABLE = request.env['hr.candidate.school']
        exist = TABLE.sudo().search([("id", "=", kwargs.get("id")), ("candidate_id", "=", kwargs.get("candidate_id"))])
        if not exist:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Object Not Found", error_code=404)
        exist.unlink()
        return DlinkHelper.JsonValidResponse(data={"detail": "OK"}, valid_code=200)
