from odoo import http
from .res_company import handle_user_company
from ..serializers.hr_applicant import HrApplicantSerializer
from ..serializers.hr_applicant_category import HrApplicantCategorySerializer
from ..serializers.hr_applicant_type import HrApplicantTypeSerializer
from ..urls import res_applicants_endpoint
from odoo.addons.dlink_api_utils import *
from odoo.http import request
from functools import wraps
from odoo.addons.dlink_api_auth.controller.decorators import token_required


def handle_applicant_company(func):
    @token_required
    @handle_user_company
    @api_key_required()
    @wraps(func)
    def wrapper(*args, company=None, **kwargs):
        applicant = request.env['hr.applicant'].with_user(request.authToken.user_id).sudo().search(
            [("id", "=", kwargs.pop("id", None)), ("company_id.id", "=", company.id)])
        if not applicant:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Applicant Not Found", error_code=404)
        kwargs["company"] = company
        kwargs["applicant"] = applicant
        return func(*args, **kwargs)

    return wrapper


class HrApplicantController(http.Controller):
    @token_required
    @api_key_required()
    @http.route("{}/types".format(res_applicants_endpoint), methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def applicantTypes(self, *args, **kwargs):

        TABLE = request.env['hr.recruitment.degree']

        return DlinkHelper.JsonValidResponse(data=HrApplicantTypeSerializer(data=TABLE.sudo().search([]), many=True).serializer())

    @token_required
    @api_key_required()
    @http.route("{}/categories".format(res_applicants_endpoint), methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def applicantCategories(self, *args, **kwargs):

        TABLE = request.env['hr.applicant.category']
        return DlinkHelper.JsonValidResponse(
            data=HrApplicantCategorySerializer(data=TABLE.sudo().search([]), many=True).serializer())

    @token_required
    @api_key_required()
    @http.route(res_applicants_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def getByCompany(self, *args, **kwargs):
        args = request.httprequest.args
        query_search = [("company_id", "=", kwargs.get("company_id"))]
        try:
            jobId = int(args.get('job', None))
            query_search.append(("job_id.id", "=", jobId)) if jobId else None
        except Exception as e:
            print("Exception", e)
            pass
        try:
            departmentId = int(args.get('department', None))
            query_search.append(("department_id.id", "=", departmentId)) if departmentId else None
        except Exception as e:
            print("Exception", e)
            pass
        paginator = PaginatorSerializer(request, "hr.applicant", query_search, HrApplicantSerializer, take=args.get('take', None),
                                        page=args.get('page', None))

        return DlinkHelper.JsonValidResponse(data=paginator.query_serializer(), meta=paginator.meta())

    @token_required
    @api_key_required()
    @handle_user_company
    @fields_required_json(fields=[
        FieldRequired(key="name", type='str'),
        FieldRequired(key="description", type='str',required=False),
        FieldRequired(key="candidate_id", type='int', relation='hr.candidate', required=False),
        FieldRequired(key="job_id", type='int', relation="hr.job"),

        FieldRequired(key="salary_expected", type='float'),
        FieldRequired(key="salary_proposed", type='float'),

        FieldRequired(key="availability", type='date'),
        FieldRequired(key="date_open", type='date'),

        FieldRequired(key="priority", type='str', choices=['0', '1', '2', '3']),
        FieldRequired(key="type_id", type='int', relation='hr.recruitment.degree', required=False),
        FieldRequired(key="categ_ids", type='int', relation='hr.applicant.category', choices=[], required=False),
        FieldRequired(key="interviewer_ids", type='int', relation='res.users', choices=[], required=False),

    ])
    @http.route(res_applicants_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, company=None, **kwargs):
        args = request.httprequest.args
        TABLE = request.env['hr.applicant']
        kwargs.update({"company_id": company.id, 'user_id': request.authToken.user_id.id})
        applicant = TABLE.with_user(request.authToken.user_id).sudo().create(kwargs)
        return DlinkHelper.JsonValidResponse(data=HrApplicantSerializer(data=applicant).serializer())

    @fields_required_json(fields=[
        FieldRequired(key="name", type='str'),
        FieldRequired(key="description", type='str', required=False),
        FieldRequired(key="candidate_id", type='int', relation='hr.candidate', required=False),
        FieldRequired(key="job_id", type='int', relation="hr.job"),

        FieldRequired(key="salary_expected", type='float'),
        FieldRequired(key="salary_proposed", type='float'),

        FieldRequired(key="availability", type='date'),
        FieldRequired(key="date_open", type='date'),

        FieldRequired(key="priority", type='str', choices=['0', '1', '2', '3']),
        FieldRequired(key="type_id", type='int', relation='hr.recruitment.degree', required=False),
        FieldRequired(key="categ_ids", type='int', relation='hr.applicant.category', choices=[], required=False),
        FieldRequired(key="interviewer_ids", type='int', relation='res.users', choices=[], required=False),

    ])
    @handle_applicant_company
    @http.route("{}/<int:id>/".format(res_applicants_endpoint), methods=["PUT"], type="json", auth="none", csrf=False, cors='*')
    def put(self, *args, company=None, applicant, **kwargs):

        applicant.with_user(request.authToken.user_id).sudo().write(kwargs)
        return DlinkHelper.JsonValidResponse(
            data=HrApplicantSerializer(data=applicant, context={"request": request}).serializer())

    @handle_applicant_company
    @http.route("{}/<int:id>/".format(res_applicants_endpoint), methods=["DELETE"], type="json", auth="none", csrf=False,
                cors='*')
    def delete(self, *args, company=None, applicant=None, **kwargs):
        applicant.with_user(request.authToken.user_id).unlink()
        return DlinkHelper.JsonValidResponse(data={"detail": "Ok"})
