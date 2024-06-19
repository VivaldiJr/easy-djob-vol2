from odoo.addons.dlink_api_utils import DlinkSerializer
from odoo.addons.ntizu_job_conn.models.company_aprovation import Representative


class NtizuRepresentativeSerializer(DlinkSerializer):
    class Meta:
        model = Representative
        fields = ['id', 'name', 'email', 'position', 'company_id', ]
