from odoo.addons.dlink_api_ntizu_job_conn.serializers.ntizu_member import NtizuMemberSerializer
from odoo.addons.dlink_api_ntizu_job_conn.serializers.ntizu_representative import NtizuRepresentativeSerializer
from odoo.addons.dlink_api_utils import DlinkSerializer
from odoo.addons.ntizu_job_conn.models.company_aprovation import Company


class NtizuCompanySerializer(DlinkSerializer):
    representative_id = NtizuRepresentativeSerializer(many=True)
    member_ids = NtizuMemberSerializer(many=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'website', 'phone', 'num_employees', 'has_hr_department', 'representative_id', 'member_ids',
                  'states', 'comment', 'company_id']
