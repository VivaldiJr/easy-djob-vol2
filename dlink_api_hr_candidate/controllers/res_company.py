from odoo.addons.dlink_api_utils import FieldRequired
from odoo.addons.dlink_api_utils import fields_required_json
from odoo.addons.dlink_api_auth.controller.decorators import token_required

from odoo.addons.dlink_api_hr_candidate.serializers.res_company import ResCompanySerializer
from odoo.addons.dlink_api_hr_candidate.urls import res_company_endpoint
from odoo.addons.dlink_api_utils import PaginatorSerializer
from odoo import http
from odoo.addons.dlink_api_utils import api_key_required, DlinkHelper
from odoo.http import request
from functools import wraps


def handle_user_company(func):
    @token_required
    @api_key_required()
    @wraps(func)
    def wrapper(*args, **kwargs):
        company, error = ResCompanyController.raiseUserCompany(request, kwargs.get("company_id", None))
        if error:
            return error
        kwargs["company"] = company
        return func(*args, **kwargs)

    return wrapper


class ResCompanyController(http.Controller):

    @staticmethod
    def raiseUserCompany(req, companyId):
        TABLE_COMPANY = request.env['res.company']
        user = req.authToken.user_id
        company = TABLE_COMPANY.sudo().search([("id", "=", companyId)])
        if not company:
            return None, DlinkHelper.JsonErrorResponse(error=[], error_message="Company Not Found", error_code=404)
        if user.company_id.id != company.id:
            return None, DlinkHelper.JsonErrorResponse(error=[], error_message="UnAuthorize", error_code=403)
        return company, None

    @token_required
    @api_key_required()
    @http.route(res_company_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        query_search = []
        q = args.get('q', None)
        query_search = [('name', 'ilike', q)] if q else query_search

        paginator = PaginatorSerializer(request, "res.company", query_search, ResCompanySerializer, take=args.get('take', None),
                                        page=args.get('page', None))

        return DlinkHelper.JsonValidResponse(data=paginator.query_serializer(), meta=paginator.meta())

    @token_required
    @api_key_required()
    @http.route("{}/<int:id>/".format(res_company_endpoint), methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def getBy(self, *args, **kwargs):
        TABLE_COMPANY = request.env['res.company']

        company = TABLE_COMPANY.sudo().search([("id", "=", kwargs['id'])])
        if not company:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Not Found", error_code=404)

        return DlinkHelper.JsonValidResponse(ResCompanySerializer(company, context={"request": request}).serializer())

    # @token_required
    @token_required
    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key="name", type="str"),
        FieldRequired(key="street", type="str", required=False),
        FieldRequired(key="zip", type="str", required=False),
        FieldRequired(key="city", type="str", required=False),
        FieldRequired(key="email", type="email", required=False),
        FieldRequired(key="phone", type="str", required=False),
        FieldRequired(key="website", type="url", required=False),
        FieldRequired(key="image", type="binary", required=False),
    ])
    @http.route("{}/<int:id>/".format(res_company_endpoint), methods=["PUT"], type="json", auth="none", csrf=False, cors='*')
    def put(self, *args, **kwargs):
        TABLE_COMPANY = request.env['res.company']

        company = TABLE_COMPANY.sudo().search([("id", "=", kwargs['id'])])
        if not company:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Not Found", error_code=404)
        company.with_user(request.authToken.user_id).sudo().write(kwargs)

        return DlinkHelper.JsonValidResponse(ResCompanySerializer(company, context={"request": request}).serializer())
