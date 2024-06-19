import datetime

from odoo.addons.dlink_api_ntizu_job_conn.serializers.ntizu_company import NtizuCompanySerializer
from odoo.addons.dlink_api_ntizu_job_conn.urls import ntizu_company_endpoint
from odoo.addons.dlink_api_utils import PaginatorSerializer
from odoo import http
from odoo.addons.dlink_api_utils import api_key_required, DlinkHelper
from odoo.addons.dlink_api_utils import fields_required_json, FieldRequired
from odoo.http import request


class NtizuCompanyController(http.Controller):
    @staticmethod
    def can_create_company(email, companyName):
        TABLE_COMPANY = request.env['res.company']
        TABLE_USER = request.env['res.users']
        user = TABLE_USER.sudo().search(["|", ("login", "=", email), ("email", "=", email)], limit=1)
        company = TABLE_COMPANY.sudo().search(["|", ("email", "=", email), ("name", "=", companyName)], limit=1)
        return len(user) == 0 and len(company) == 0

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key="email", type="email"),
        FieldRequired(key="token", type="str"),
    ])
    @http.route("{}/verify_email".format(ntizu_company_endpoint), methods=["POST"], type="json", auth="none", csrf=False,
                cors='*')
    def verify_email(self, *args, **kwargs):

        TABLE = request.env['ntizu.company.request.token']

        token = TABLE.sudo().search([("email", "=", kwargs.get("email", None)), ("token", "=", kwargs.get("token", None))])

        if token:
            if token.has_expired():
                return DlinkHelper.JsonErrorResponse(error=[], error_message="Token expired", error_code=403)
            TABLE_COMPANY = request.env['ntizu.company.request']
            company = TABLE_COMPANY.sudo().search([("representative_id.email", "=", kwargs.get("email", None))])

            if len(company) != 1:
                return DlinkHelper.JsonErrorResponse(error=[],
                                                     error_message="Something is wrong with your email, you can only be a representative of a company")

            if company.states != 'draft':
                return DlinkHelper.JsonErrorResponse(error=[], error_message="This company already exist in proceess")
            company.update({"states": "pending"})
            token.update({"token_expiry_date": datetime.datetime.now()})
            return DlinkHelper.JsonValidResponse(data=NtizuCompanySerializer(data=company).serializer())
        return DlinkHelper.JsonErrorResponse(error=[], error_message="Wrong Token or Email", error_code=403)

    @api_key_required()
    @http.route(ntizu_company_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        query_search = []
        q = args.get('q', None)
        query_search = [('name', 'ilike', q)] if q else query_search

        paginator = PaginatorSerializer(request, "ntizu.company.request", query_search, NtizuCompanySerializer,
                                        take=args.get('take', None), page=args.get('page', None))
        return DlinkHelper.JsonValidResponse(data=paginator.query_serializer(), meta=paginator.meta())

    @api_key_required()
    @http.route("{}/<int:id>/".format(ntizu_company_endpoint), methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def getBy(self, *args, **kwargs):
        TABLE_COMPANY = request.env['ntizu.company.request']

        company = TABLE_COMPANY.sudo().search([("id", "=", kwargs['id'])])
        if not company:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Not Found", error_code=404)

        return DlinkHelper.JsonValidResponse(NtizuCompanySerializer(company, context={"request": request}).serializer())

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key="provider", type='str', required=False),

        FieldRequired(key="name", type='str'),
        FieldRequired(key="website", type='url'),
        FieldRequired(key="phone", type='str'),
        FieldRequired(key="num_employees", type='int'),
        FieldRequired(key="has_hr_department", type='bool'),
        FieldRequired(key="comment", type='str'),
        FieldRequired(key="currency_id", type='int', relation='res.currency'),
        FieldRequired(key="member_ids", type='dict', choices=[], required=False, fields=[
            FieldRequired(key="name", type='str'),
            FieldRequired(key="email", type='email'),
        ]),
        FieldRequired(key="representative_id", type='dict', choices=[], fields=[
            FieldRequired(key="name", type='str'),
            FieldRequired(key="email", type='email'),
            FieldRequired(key="password", type='str'),
            FieldRequired(key="position", type='str'),
        ]),

    ])
    @http.route(ntizu_company_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, **kwargs):
        TABLE_TOKEN = request.env['ntizu.company.request.token']
        emails = [r.get("email", None) for r in kwargs.get("representative_id", [])]

        for email in emails:
            if not NtizuCompanyController.can_create_company(email=email, companyName=kwargs['name']):
                return DlinkHelper.JsonErrorResponse(error=[], error_message="Can't create this company")

        TABLE_NTIZU_COMPANY = request.env['ntizu.company.request']
        TABLE_NTIZU_REPRESENTATIVE = request.env['representative.ntizu.company.request']
        TABLE_NTIZU_MEMBER = request.env['member.ntizu.company.request']
        provider = kwargs.pop("provider", None)
        exist = TABLE_NTIZU_COMPANY.sudo().search([("representative_id.email", "in", emails)])
        if exist:
            if exist.states != 'draft':
                return DlinkHelper.JsonErrorResponse(error=[], error_message="This company already exist in proceess")
            exist.unlink()

        members = kwargs.pop("member_ids", [])
        representatives = kwargs.pop("representative_id", [])
        company = TABLE_NTIZU_COMPANY.sudo().create(kwargs)

        for representative in representatives:
            representative['company_id'] = company.id
            TABLE_NTIZU_REPRESENTATIVE.sudo().create(representative)
        for member in members:
            member['company_id'] = company.id
            TABLE_NTIZU_MEMBER.sudo().create(member)

        for email in emails:
            TABLE_TOKEN.sudo().create({
                "email": email,
                "provider": provider
            })
        return DlinkHelper.JsonValidResponse({"detail": "All Representatives verify your email"})

    @api_key_required()
    @http.route("{}/me".format(ntizu_company_endpoint), methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def my_companies(self, *args, **kwargs):
        args = request.httprequest.args
        email = args.get("email", None)
        TABLE_NTIZU_REPRESENTATIVES = request.env['representative.ntizu.company.request']

        companies = TABLE_NTIZU_REPRESENTATIVES.sudo().search([("email", "=", email)]).mapped('company_id')
        return DlinkHelper.JsonValidResponse(data=NtizuCompanySerializer(data=companies).serializer())
