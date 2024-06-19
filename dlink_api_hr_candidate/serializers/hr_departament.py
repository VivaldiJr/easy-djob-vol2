from odoo.addons.dlink_api_hr_candidate.serializers.res_company import ResCompanySerializer
from odoo.addons.dlink_api_utils import DlinkSerializer
from odoo.addons.hr.models.hr_department import Department


class HrDepartamentSerializer(DlinkSerializer):
    company_id = ResCompanySerializer()

    class Meta:
        model = Department
        fields = ['id', 'name', 'member_ids', 'jobs_ids', 'complete_name', 'company_id', 'parent_id', 'child_ids',
                  'master_department_id',
                  'parent_id',
                  'manager_id',
                  'total_employee', 'jobs_ids','website', 'location', 'description' ]
