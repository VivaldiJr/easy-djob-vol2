from odoo import http
from .res_company import handle_user_company
from ..serializers.hr_employee import HrEmployeeSerializer
from ..urls import res_employees_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request
from odoo.addons.dlink_api_auth.controller.decorators import token_required
from functools import wraps


def handle_employee_company(func):
    @token_required
    @handle_user_company
    @api_key_required()
    @wraps(func)
    def wrapper(*args, company=None, **kwargs):
        employee = request.env['hr.employee'].with_user(request.authToken.user_id).sudo().search(
            [("id", "=", kwargs.pop("id", None)), ("company_id.id", "=", company.id)])
        if not employee:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Employee Not Found", error_code=404)
        kwargs["company"] = company
        kwargs["employee"] = employee
        return func(*args, **kwargs)

    return wrapper


class HrEmployeeController(http.Controller):
    @token_required
    @api_key_required()
    @http.route(res_employees_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args
        company_id = kwargs.get("company_id")

        if not company_id:
            return DlinkHelper.JsonErrorResponse(message="Company ID is required")

        # Construir a consulta de pesquisa
        query_search = [("company_id", "=", company_id), "|", ("name", "ilike", args.get("q", "")),
                        ("private_email", "ilike", args.get("q", ""))]

        paginator = PaginatorSerializer(request, "hr.employee", query_search, HrEmployeeSerializer,
                                        take=args.get('take', None), page=args.get('page', None))

        return DlinkHelper.JsonValidResponse(data=paginator.query_serializer(), meta=paginator.meta())

    @token_required
    @api_key_required()
    @handle_user_company
    @fields_required_json(fields=[
        FieldRequired(key="name", type='str'),
        FieldRequired(key="work_email", type='email'),
        FieldRequired(key="phone", type='str'),
        FieldRequired(key="birthday", type='date'),
        FieldRequired(key="gender", type='str', choices=['male', 'female', 'other']),
        FieldRequired(key="job_id", type='int', relation="hr.job", required=False),
        FieldRequired(key="avatar_256", type='binary', required=False),

    ])
    @http.route(res_employees_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, company=None, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.employee']
        kwargs.update({"company_id": company.id})
        if TABLE.sudo().search([("work_email", "=", kwargs.get("work_email"))]):
            return DlinkHelper.JsonErrorResponse(error_message="Email already taked", error=[])
        employee = TABLE.with_user(request.authToken.user_id).sudo().create(kwargs)
        return DlinkHelper.JsonValidResponse(data=HrEmployeeSerializer(data=employee).serializer())

    @fields_required_json(fields=[
        FieldRequired(key="name", type='str', required=False),
        FieldRequired(key="work_email", type='email', required=False),
        FieldRequired(key="phone", type='str', required=False),
        FieldRequired(key="birthday", type='date', required=False),
        FieldRequired(key="gender", type='str', choices=['male', 'female', 'other'], required=False),
        FieldRequired(key="job_id", type='int', relation="hr.job", required=False),
        FieldRequired(key="avatar_256", type='binary', required=False),

    ])
    @handle_employee_company
    @http.route("{}/<int:id>/".format(res_employees_endpoint), methods=["PUT"], type="json", auth="none", csrf=False, cors='*')
    def put(self, *args, company=None, employee, **kwargs):

        TABLE = request.env['hr.employee']
        exist = TABLE.sudo().search([("work_email", "=", kwargs.get("work_email"))])
        if exist and exist[0].id != employee.id:
            return DlinkHelper.JsonErrorResponse(error_message="Email already taked", error=[])
        employee.with_user(request.authToken.user_id).sudo().write(kwargs)
        return DlinkHelper.JsonValidResponse(
            data=HrEmployeeSerializer(data=employee, context={"request": request}).serializer())

    @handle_employee_company
    @http.route("{}/<int:id>/".format(res_employees_endpoint), methods=["DELETE"], type="json", auth="none", csrf=False,
                cors='*')
    def delete(self, *args, company=None, employee=None, **kwargs):
        employee.with_user(request.authToken.user_id).unlink()
        return DlinkHelper.JsonValidResponse(data={"detail": "Ok"})
