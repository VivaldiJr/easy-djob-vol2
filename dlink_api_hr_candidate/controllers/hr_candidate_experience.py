from odoo import http
from ..serializers.hr_candidate_experience import HrCandidateExperienceSerializer
from ..urls import hr_candidate_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request


class HrCandidateExperienceController(http.Controller):
    @api_key_required()
    @http.route("{}/<int:candidate_id>/experience".format(hr_candidate_endpoint), methods=["GET"], type="json", auth="none",
                csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.candidate.experience']
        return DlinkHelper.JsonValidResponse(
            data=HrCandidateExperienceSerializer(data=TABLE.sudo().search([("candidate_id", "=", kwargs.get("candidate_id", 0))]),
                                                 many=True).serializer())

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key='start_date', type='datetime'),
        FieldRequired(key='end_date', type='datetime'),
        FieldRequired(key='company', type='int', relation="hr.company"),
        FieldRequired(key='job_positions', type='int', relation="hr.job_position"),
        FieldRequired(key='achievements', type='str', required=False),
    ])
    @http.route("{}/<int:candidate_id>/experience".format(hr_candidate_endpoint), methods=["POST"], type="json", auth="none",
                csrf=False, cors='*')
    def post(self, *args, **kwargs):
        print(kwargs)
        TABLE = request.env['hr.candidate.experience']
        candidate_exp = TABLE.sudo().create(kwargs)
        return DlinkHelper.JsonValidResponse(data=HrCandidateExperienceSerializer(data=candidate_exp).serializer(),
                                             valid_code=201)

    @http.route("{}/<int:candidate_id>/experience/<int:id>".format(hr_candidate_endpoint), methods=["DELETE"], type="json",
                auth="none",
                csrf=False, cors='*')
    def delete(self, *args, **kwargs):
        TABLE = request.env['hr.candidate.experience']
        exist = TABLE.sudo().search([("id", "=", kwargs.get("id")), ("candidate_id", "=", kwargs.get("candidate_id"))])
        if not exist:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Object Not Found", error_code=404)
        exist.unlink()
        return DlinkHelper.JsonValidResponse(data={"detail": "OK"}, valid_code=200)
