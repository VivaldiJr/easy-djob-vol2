from odoo import http
from ..serializers.mail_activity import MailActivitySerializer
from ..urls import res_activities_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request
from odoo.addons.dlink_api_auth.controller.decorators import token_required


class HrActivityController(http.Controller):
    @token_required
    @api_key_required()
    @http.route(res_activities_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        query_search = [("user_id.company_id.id", "=", kwargs.get("company_id")), ("res_model", "=", "hr.applicant")]
        paginator = PaginatorSerializer(request, "mail.activity", query_search, MailActivitySerializer,
                                        take=args.get('take', None),
                                        page=args.get('page', None))

        return DlinkHelper.JsonValidResponse(data=paginator.query_serializer(), meta=paginator.meta())



