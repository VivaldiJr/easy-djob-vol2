from odoo import http
from odoo.addons.dlink_api_utils import *
from odoo.http import request
import base64
from werkzeug.wrappers import Response
import filetype


class FilesController(http.Controller):
    @api_key_required(isHttp=True)
    @http.route("/files/<string:model>/<int:id>/<string:field>/", methods=["GET"], type="http", auth="none", csrf=False, cors='*')
    def get(self, **kwargs):
        model = kwargs['model']
        id = kwargs['id']
        field = kwargs['field']
        try:

            registro = request.env[model].sudo().browse(int(id))
            if getattr(registro, field):
                contenido = base64.b64decode(getattr(registro, field))
                mime = filetype.guess_mime(contenido)
                respuesta = Response(status=200)
                respuesta.stream.write(contenido)
                respuesta.stream.flush()
                if not mime:
                    mime = 'image/svg+xml' if str(respuesta.data).__contains__("SVG") else mime
                respuesta.content_type = mime
                return respuesta
            else:
                return DlinkHelper.JsonErrorResponse(isHttp=True, error=[], error_code=404)
        except Exception as e:
            return DlinkHelper.JsonErrorResponse(error=e, error_message=str(e), isHttp=True)

    @api_key_required(isHttp=True)
    @fields_required_json(fields=[
        FieldRequired(key='attachment', type='file')
    ], isHttp=True)
    @http.route("/files/base64", methods=["POST"], type="http", auth="none", csrf=False, cors='*')
    def post(self, **kwargs):
        encode = None
        if kwargs.get('attachment', None):
            file = kwargs.get('attachment')
            attachment = file.read()
            encode = base64.b64encode(attachment)

        return DlinkHelper.JsonValidResponse(data={"base64": encode.decode('utf-8')}, isHttp=True)
