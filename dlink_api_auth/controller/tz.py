import pytz

from odoo import http
from ..urls import timezone_endpoint
from odoo.addons.dlink_api_utils import *


class JsonDLinkTimeZone(http.Controller):
    @staticmethod
    def timezones():
        return [tz for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]

    @api_key_required()
    @http.route(timezone_endpoint, methods=["GET"], type="json", auth="none", csrf=False, cors='*')
    def get(self, *args, **kwargs):
        return DlinkHelper.JsonValidResponse(data=JsonDLinkTimeZone.timezones())
