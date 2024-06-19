from odoo.addons.dlink_api_utils import DlinkSerializer
from odoo.addons.ntizu_job_conn.models.company_aprovation import Member


class NtizuMemberSerializer(DlinkSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name', 'email', 'company_id', ]
