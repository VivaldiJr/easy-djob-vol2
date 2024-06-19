from odoo import http
from .res_company import handle_user_company
from ..serializers.hr_job_position import HrJobSerializer

from ..urls import hr_applicant_endpoint, res_jobs_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request
from odoo.addons.dlink_api_auth.controller.decorators import token_required
from functools import wraps


def handle_job_company(func):
    @token_required
    @handle_user_company
    @api_key_required()
    @wraps(func)
    def wrapper(*args, company=None, **kwargs):
        job = request.env['hr.job'].with_user(request.authToken.user_id).sudo().search(
            [("id", "=", kwargs.pop("id", None)), ("company_id.id", "=", company.id)])
        if not job:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Job Not Found", error_code=404)
        kwargs["company"] = company
        kwargs["job"] = job
        return func(*args, **kwargs)

    return wrapper


class HrJobController(http.Controller):
    @token_required
    @api_key_required()
    @http.route("{}/job".format(hr_applicant_endpoint), methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def find(self, *args, **kwargs):
        args = request.httprequest.args
        query_search = []
        q = args.get('q', "")
        query_search = ["|", "|", ('name', 'ilike', q), ("company_id.name", 'ilike', q),
                        ("department_id.name", "ilike", q)] if q else query_search

        address = args.get('address', "")
        if address:
            query_search.append(("address_id", "ilike", address if address != "Remote" else None))
        query_search.append(("active", "=", True))

        paginator = PaginatorSerializer(request, "hr.job", query_search, HrJobSerializer, take=args.get('take', None),
                                        page=args.get('page', None))

        return DlinkHelper.JsonValidResponse(data=paginator.query_serializer(), meta=paginator.meta())

    @handle_user_company
    @http.route(res_jobs_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, company=None, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.job']
        query_search = [("company_id", "=", company.id), ("name", "ilike", args.get("q", ""))]
        try:
            query_search.append(("department_id.id", "=", int(args.get('department', None))))
        except:
            pass

        return DlinkHelper.JsonValidResponse(
            data=HrJobSerializer(data=TABLE.sudo().search(query_search), many=True, context={'request': request}).serializer())

    @fields_required_json(fields=[
        FieldRequired(key="name", type='str'),
        FieldRequired(key="description", type='str'),
        FieldRequired(key="requirements", type='str'),
        FieldRequired(key="no_of_recruitment", type='int', required=False),
        FieldRequired(key="department_id", type='int', relation='hr.department'),
        FieldRequired(key="contract_type_id", type='int', relation='hr.contract.type'),

    ])
    @handle_user_company
    @http.route(res_jobs_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, company=None, **kwargs):
        TABLE = request.env['hr.job']
        kwargs.update({"company_id": company.id})
        job = TABLE.with_user(request.authToken.user_id).sudo().create(kwargs)
        return DlinkHelper.JsonValidResponse(
            data=HrJobSerializer(data=job, context={"request": request}).serializer())

    @fields_required_json(
        fields=[
            FieldRequired(key="name", type='str'),
            FieldRequired(key="description", type='str', required=False),
            FieldRequired(key="requirements", type='str', required=False),
            FieldRequired(key="no_of_recruitment", type='int', required=False),
            FieldRequired(key="contract_type_id", type='int', relation='hr.contract.type', required=False),

        ],
        decline=['department_id']
    )
    @handle_job_company
    @http.route("{}/<int:id>/".format(res_jobs_endpoint), methods=["PUT"], type="json", auth="none", csrf=False, cors='*')
    def put(self, *args, company=None, job=None, **kwargs):
        print(kwargs)
        job.with_user(request.authToken.user_id).sudo().update(kwargs)
        return DlinkHelper.JsonValidResponse(
            data=HrJobSerializer(data=job, context={"request": request}).serializer())

    @handle_job_company
    @http.route("{}/<int:id>/".format(res_jobs_endpoint), methods=["DELETE"], type="json", auth="none", csrf=False,
                cors='*')
    def delete(self, *args, company=None, job=None, **kwargs):
        job.with_user(request.authToken.user_id).unlink()
        return DlinkHelper.JsonValidResponse(data={"detail": "Ok"})
