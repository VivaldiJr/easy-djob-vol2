import datetime

from odoo import http
from ..models.res_users_inherit import ResUsersInherit
from ..serializers.hr_applicant import HrApplicantSerializer
from ..serializers.hr_candidate import HrCandidateSerializer
from ..urls import hr_candidate_endpoint

from odoo.addons.dlink_api_utils import *
from odoo.http import request


class HrCandidateController(http.Controller):

    @staticmethod
    def can_create_candidate(email):
        TABLE_USER = request.env['res.users']
        TABLE_CANTIDATE = request.env['hr.candidate']
        candidate = TABLE_CANTIDATE.sudo().search([("email", "=", email)])
        user = TABLE_USER.sudo().search(["|", ("email", "=", email), ("login", "=", email)])
        return not ((candidate and candidate.email_verified) or user)

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key="email", type="email"),
        FieldRequired(key="token", type="str"),
        FieldRequired(key="company", type="int", relation="res.company", required=False),
    ])
    @http.route("{}/verify_email".format(hr_candidate_endpoint), methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def verify_email(self, *args, **kwargs):
        TABLE = request.env['hr.candidate.token']
        TABLE_CANTIDATE = request.env['hr.candidate']
        TABLE_COMPANY = request.env['res.company']
        company = TABLE_COMPANY.sudo().search([("id", "=", kwargs.get('company', 1))], limit=1)
        if not company:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Company Wrong")

        token = TABLE.sudo().search([("email", "=", kwargs.get("email", None)), ("token", "=", kwargs.get("token", None))])
        if token:
            if token.has_expired():
                return DlinkHelper.JsonErrorResponse(error=[], error_message="Token expired", error_code=403)
            if not HrCandidateController.can_create_candidate(kwargs['email']):
                return DlinkHelper.JsonErrorResponse(error=[], error_message="Can't complete register for this candidate")
            candidate = TABLE_CANTIDATE.sudo().search([("email", "=", kwargs.get("email", None))])
            Table_resouce = request.env['resource.resource'].sudo().search([], order='id', limit=1)

            if candidate and Table_resouce:
                if candidate.email_verified:
                    return DlinkHelper.JsonErrorResponse(error=[], error_message="Candidate already email verified",
                                                         error_code=403)
                candidate.sudo().write({"email_verified": True})

                ResUsersInherit.getOrCreateUser(request, candidate.email, "{} {}".format(candidate.name, candidate.last_name),
                                                token.password )

                token.update({"token_expiry_date": datetime.now()})
                return DlinkHelper.JsonValidResponse(data=HrCandidateSerializer(data=candidate).serializer())
        return DlinkHelper.JsonErrorResponse(error=[], error_message="Wrong Token or Email", error_code=403)

    @api_key_required()
    @http.route(hr_candidate_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        args = request.httprequest.args

        query_search = []
        q = args.get('q', None)
        query_search = ['|', '|', '|', ('name', 'ilike', q), ('last_name', 'ilike', q), ('email', 'ilike', q),
                        ('professional_title', 'ilike', q)] if q else query_search

        age = int(args.get('age')) if args.get('age', None) else None
        query_search = ["&", *query_search, ("age", "=", age)] if len(query_search) > 0 else [
            ("age", "=", age)] if age else query_search

        country = args.get('country', None)
        query_search = ["&", *query_search, ("country_id.id", "=", country)] if len(query_search) > 0 else [
            ("country_id.id", "=", country)] if country else query_search

        highest_education_level = args.get('highest_education_level', None)
        query_search = ["&", *query_search, ("highest_education_level", "=", highest_education_level)] if len(
            query_search) > 0 else [
            ("highest_education_level", "=", highest_education_level)] if highest_education_level else query_search

        study_area = args.get('study_area', None)
        query_search = ["&", *query_search, ("school_ids.study_area.id", "=", study_area)] if len(query_search) > 0 else [
            ("school_ids.study_area.id", "=", study_area)] if study_area else query_search
        paginator = PaginatorSerializer(request, "hr.candidate", query_search, HrCandidateSerializer, take=args.get('take', None),
                                        page=args.get('page', None))
        return DlinkHelper.JsonValidResponse(data=paginator.query_serializer(), meta=paginator.meta())

    @api_key_required()
    @http.route("{}/<int:id>/".format(hr_candidate_endpoint), methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def getBy(self, *args, **kwargs):
        TABLE_CANDIDATE = request.env['hr.candidate']

        candidate = TABLE_CANDIDATE.sudo().search([("id", "=", kwargs['id'])])
        if not candidate:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Not Found", error_code=404)

        return DlinkHelper.JsonValidResponse(HrCandidateSerializer(candidate, context={"request": request}).serializer())

    @api_key_required()
    @http.route("{}/search".format(hr_candidate_endpoint), methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def getByEmail(self, *args, **kwargs):
        args = request.httprequest.args
        TABLE_CANDIDATE = request.env['hr.candidate']

        candidate = TABLE_CANDIDATE.sudo().search([("email", "=", args.get("email", None))], limit=1)
        if not candidate:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Not Found", error_code=404)

        return DlinkHelper.JsonValidResponse(HrCandidateSerializer(candidate, context={"request": request}).serializer())

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key="name", type="str"),
        FieldRequired(key="last_name", type="str"),
        FieldRequired(key="password", type="str"),
        FieldRequired(key="address", type="str"),
        FieldRequired(key="email", type="email"),

        FieldRequired(key="provider", type="str", required=False),
        FieldRequired(key="country_id", type="int", relation="res.country"),
    ])
    @http.route(hr_candidate_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def post(self, *args, **kwargs):
        TABLE = request.env['hr.candidate']
        TABLE_TOKEN = request.env['hr.candidate.token']
        password = kwargs.pop('password', None)
        provider = kwargs.pop("provider", None)

        if not HrCandidateController.can_create_candidate(kwargs['email']):
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Can't create this candidate")

        # Primeiro cria ou atualiza o candidato
        candidate = TABLE.sudo().search([("email", "=", kwargs.get("email", None))])
        if candidate:
            candidate.write(kwargs)
        else:
            candidate = TABLE.sudo().create(kwargs)

        # Depois cria o token para o candidato
        TABLE_TOKEN.sudo().create({"email": candidate.email, "provider": provider, "password": password})

        return DlinkHelper.JsonValidResponse({"detail": "Verify email"})

    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key="professional_title", type="str"),
        FieldRequired(key="professional_description", type="str"),
        FieldRequired(key="age", type="int"),
        FieldRequired(key="address", type="str"),
        FieldRequired(key="postal_code", type="str"),
        FieldRequired(key="city_province", type="str"),
        FieldRequired(key="phone", type="str"),
        FieldRequired(key="resume_option", type="str", choices=['linkedin', 'file', 'manual']),
        FieldRequired(key="skill_ids", type="int", choices=[], relation="hr.skill", required=False),

    ])
    @http.route("{}/<int:id>".format(hr_candidate_endpoint), methods=["PUT"], type="json", auth="none", csrf=False, cors='*')
    def put(self, *args, **kwargs):
        TABLE = request.env['hr.candidate']
        candidate = TABLE.sudo().search([("id", "=", kwargs.get("id", None))])
        if not candidate:
            return DlinkHelper.JsonErrorResponse(error=[], error_message="Object Not Found", error_code=404)

        candidate.write(kwargs)
        return DlinkHelper.JsonValidResponse(
            data=HrCandidateSerializer(data=candidate, context={"request": request}).serializer())
