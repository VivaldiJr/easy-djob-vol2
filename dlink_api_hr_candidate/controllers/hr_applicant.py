from odoo import http
from ..serializers.hr_applicant import HrApplicantSerializer
from ..urls import hr_applicant_endpoint

from odoo.addons.dlink_api_utils import *
from odoo.http import request
from odoo.addons.dlink_api_auth.controller.decorators import token_required


class HrApplicantController(http.Controller):
    @token_required
    @api_key_required()
    @http.route(hr_applicant_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        user = request.authToken.user_id
        args = request.httprequest.args
        query_search = []
        q = args.get('q', None)
        query_search = [('name', 'ilike', q)] if q else query_search
        query_search.append(("candidate_id", "=", user.candidate_id.id if user.candidate_id else None))
        paginator = PaginatorSerializer(request, "hr.applicant", query_search, HrApplicantSerializer, take=args.get('take', None),
                                        page=args.get('page', None))

        return DlinkHelper.JsonValidResponse(data=paginator.query_serializer(), meta=paginator.meta())

    @token_required
    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key="description", type='str', required=False)
    ])
    @http.route(hr_applicant_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, **kwargs):
        user = request.authToken.user_id
        TABLE = request.env['hr.applicant']
        if not user.candidate_id:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="No candidate for applicant to job")
        kwargs.update({
            "user_id": user.id,
            "name": user.partner_id.name,
            "partner_id": user.partner_id.id,
            'candidate_id': user.candidate_id.id
        })
        applicant = TABLE.with_user(user).sudo().create(kwargs)
        return DlinkHelper.JsonValidResponse(data=HrApplicantSerializer(data=applicant, context={"request":request}).serializer())
