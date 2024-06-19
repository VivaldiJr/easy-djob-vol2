from odoo import http
from .res_company import handle_user_company
from ..serializers.hr_departament import HrDepartamentSerializer
from ..urls import res_department_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request
from odoo.addons.dlink_api_auth.controller.decorators import token_required
from functools import wraps


def handle_department_company(func):
    @token_required
    @handle_user_company
    @api_key_required()
    @wraps(func)
    def wrapper(*args, company=None, **kwargs):
        department = request.env['hr.department'].with_user(request.authToken.user_id).sudo().search(
            [("id", "=", kwargs.pop("id", None)), ("company_id.id", "=", company.id)])
        if not department:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Department Not Found", error_code=404)
        kwargs["company"] = company
        kwargs["department"] = department
        return func(*args, **kwargs)

    return wrapper


class HrDepartmentController(http.Controller):

    @handle_user_company
    @http.route(res_department_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, company=None, **kwargs):
        TABLE = request.env['hr.department']
        args = request.httprequest.args
        query_search = [("company_id.id", "=", company.id), ("name", "ilike", args.get("q", ""))]
        return DlinkHelper.JsonValidResponse(
            data=HrDepartamentSerializer(data=TABLE.sudo().search(query_search), many=True).serializer())

    @fields_required_json(fields=[
        FieldRequired(key="name", type='str'),
        FieldRequired(key="parent_id", type='int', relation='hr.department', required=False),
    ])

    @handle_user_company
    @http.route(res_department_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, company=None, **kwargs):
        TABLE = request.env['hr.department']

        # Adicione os novos campos ao dicionário kwargs
        kwargs.update({
            "company_id": company.id,
            "website": kwargs.get("website"),
            "location": kwargs.get("location"),
            "description": kwargs.get("description")
        })

        try:
            department = TABLE.with_user(request.authToken.user_id).sudo().create(kwargs)
            return DlinkHelper.JsonValidResponse(
                data=HrDepartamentSerializer(data=department, context={"request": request}).serializer())
        except ValidationError as e:
            return DlinkHelper.JsonInvalidResponse(message=e.name)


    @fields_required_json(fields=[
        FieldRequired(key="name", type='str'),
        FieldRequired(key="parent_id", type='int', relation='hr.department', required=False),
    ])
    @handle_department_company
    @http.route("{}/<int:id>/".format(res_department_endpoint), methods=["PUT"], type="json", auth="none", csrf=False, cors='*')
    def put(self, *args, company=None, department, **kwargs):
        department.with_user(request.authToken.user_id).sudo().write(kwargs)
        print(kwargs)
        return DlinkHelper.JsonValidResponse(
            data=HrDepartamentSerializer(data=department, context={"request": request}).serializer())

    @handle_department_company
    @http.route("{}/<int:id>/".format(res_department_endpoint), methods=["DELETE"], type="json", auth="none", csrf=False,
                cors='*')
    def delete(self, *args, company=None, department=None, **kwargs):
        department.with_user(request.authToken.user_id).unlink()
        return DlinkHelper.JsonValidResponse(data={"detail": "Ok"})
