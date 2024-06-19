from odoo import http
from .decorators import header_authorization
from ..controller.decorators import token_required
from ..serializers.token import TokenSerializer
from ..serializers.user import UserSerializer
from ..urls import *
from odoo.exceptions import AccessError, AccessDenied
from odoo.http import request

from odoo.addons.dlink_api_utils import *
import requests


class JsonDLinkAccessToken(http.Controller):
    @api_key_required()
    @headers_required_json(headers={header_device: "identificador unico del móvil", })
    @fields_required_json(fields=[
        FieldRequired(key="username", type="str"),
        FieldRequired(key="password", type="str")
    ])
    @http.route(tokenAuth_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def signIn(self, username, password, **kwargs):
        TABLE_API_AUTH_TOKEN = request.env['dlink_auth_api.access_token']
        TABLE_USER = request.env['res.users']
        TABLE_CANDIDATE = request.env['hr.candidate']
        kwargs.update(request.get_http_params())
        headers = request.httprequest.headers
        db, device = (request.env.registry.db_name, headers.get(header_device))
        print(db, device)
        try:
            if username == 'google-signIn':
                user = verify_google_id_token(password)
            else:
                user = TABLE_USER.sudo().search([("login", "=", username)])
                user.authenticate(db, user.login, password, {})

            candidate = TABLE_CANDIDATE.sudo().search([("email", "=", user.email)])
            if candidate:
                if not candidate.email_verified:
                    pass
                    # raise AccessDenied("Candidate email no verify")

            access_token = TABLE_API_AUTH_TOKEN.find_or_create_token(user_id=user.id, device=device, create=True)
            access_tokens_obj = TABLE_API_AUTH_TOKEN.sudo().search([("token", "=", access_token)])

            return DlinkHelper.JsonValidResponse(TokenSerializer(access_tokens_obj, context={"request": request}).serializer())

        except AccessError as aee:
            print("AccessError")
            return DlinkHelper.JsonErrorResponse([], error_message=str(aee), error_code=403)

        except AccessDenied as ade:
            print("AccessDenied")
            return DlinkHelper.JsonErrorResponse([], error_message=str(ade), error_code=401)

        except Exception as e:
            print("Exception")
            return DlinkHelper.JsonErrorResponse([], error_message=str(e), error_code=403)

    @headers_required_json(headers={header_device: "identificador unico del móvil"})
    @fields_required_json(fields=[
        FieldRequired(key="refresh", type='str')
    ])
    @http.route(tokenRefresh_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def refreshToken(self, **body):
        TABLE_API_AUTH_TOKEN = request.env['dlink_auth_api.access_token']
        refresh_token = body.get('refresh', None)
        device_id = request.httprequest.headers.get(header_device)
        query_search = [("refresh", "=", refresh_token), ("device", "=", device_id)]
        access_token_data = TABLE_API_AUTH_TOKEN.sudo().search(query_search, order="id DESC", limit=1)
        if access_token_data and not access_token_data.has_refresh_expired():
            token = access_token_data.refresh_token()
            return DlinkHelper.JsonValidResponse(TokenSerializer(token, context={"request": request}).serializer())
        return DlinkHelper.JsonErrorResponse([{"key": header_authorization, "data": "Refresh Expired"}], error_code=401)

    @token_required
    @http.route(tokenVerify_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def verifyToken(self, **kwargs):
        return DlinkHelper.JsonValidResponse(
            UserSerializer(data=request.authToken.user_id, context={"request": request}).serializer())

    @token_required
    @http.route(tokenRemove_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def logOut(self, **post):
        request.authToken.unlink()
        return DlinkHelper.JsonValidResponse({"detail": "OK"})

    @token_required
    @api_key_required()
    @fields_required_json(fields=[
        FieldRequired(key='old_password', type='str'),
        FieldRequired(key='new_password', type='str'),
    ])
    @http.route(changePassword_endpoint, methods=["POST"], type="json", auth="none", csrf=False, cors='*')
    def change_password(self, old_password, new_password, **kwargs):
        user = request.authToken.user_id
        headers = request.httprequest.headers
        db = request.env.registry.db_name
        try:
            user.authenticate(db, user.login, old_password, {})
            user.write({'password': new_password, "new_password": new_password})
            return DlinkHelper.JsonValidResponse(data=UserSerializer(data=user, context={'request': request}).serializer())
        except AccessError as aee:
            return DlinkHelper.JsonErrorResponse([], error_message=str(aee), error_code=403)
        except AccessDenied as ade:
            return DlinkHelper.JsonErrorResponse([], error_message="Contraseña actual incorrecta", error_code=401)
        except Exception as e:
            return DlinkHelper.JsonErrorResponse([], error_message=str(e), error_code=403)


def verify_google_id_token(token) -> str:
    TABLE_USER = request.env['res.users']
    try:
        url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            user_email = data.get('email')
            user = TABLE_USER.sudo().search([("login", "=", user_email)])
            if user:
                return user
    except requests.exceptions.RequestException as e:
        print(e)
    raise AccessDenied
