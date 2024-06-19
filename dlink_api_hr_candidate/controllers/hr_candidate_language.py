from odoo import http
from ..serializers.hr_candidate_language import HrCandidateLanguageSerializer
from ..urls import hr_candidate_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request


class HrCandidateLanguageController(http.Controller):
    @api_key_required()
    @http.route("{}/<int:candidate_id>/language".format(hr_candidate_endpoint), methods=["GET"], type="json", auth="none",
                csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.candidate.language']
        return DlinkHelper.JsonValidResponse(
            data=HrCandidateLanguageSerializer(data=TABLE.sudo().search([("candidate_id", "=", kwargs.get("candidate_id", 0))]),
                                               many=True).serializer())

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key='language', type='int', relation="hr.language"),
        FieldRequired(key='level', type='str', choices=['basic', 'intermediate', 'advanced']),
    ])
    @http.route("{}/<int:candidate_id>/language".format(hr_candidate_endpoint), methods=["POST"], type="json", auth="none",
                csrf=False, cors='*')
    def post(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.candidate.language']
        candidate_lang = TABLE.sudo().create(kwargs)
        return DlinkHelper.JsonValidResponse(data=HrCandidateLanguageSerializer(data=candidate_lang).serializer(), valid_code=201)

    @http.route("{}/<int:candidate_id>/language/<int:id>".format(hr_candidate_endpoint), methods=["DELETE"], type="json",
                auth="none",
                csrf=False, cors='*')
    def delete(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.candidate.language']
        exist = TABLE.sudo().search([("id", "=", kwargs.get("id")), ("candidate_id", "=", kwargs.get("candidate_id"))])
        if not exist:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Object Not Found", error_code=404)
        exist.unlink()
        return DlinkHelper.JsonValidResponse(data={"detail": "OK"}, valid_code=200)
