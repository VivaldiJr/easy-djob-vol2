from odoo.addons.dlink_api_utils.utils.domain import domain
from odoo.addons.dlink_api_hr_candidate.serializers.hr_job_position import HrJobSerializer
from odoo.addons.hr.models.hr_employee import HrEmployeePrivate
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrEmployeeSerializer(DlinkSerializer):
    job_id = HrJobSerializer()

    class Meta:
        model = HrEmployeePrivate
        fields = ['id', 'name', 'work_email', 'gender', 'company_id', 'birthday', 'phone', 'job_id']

        functions = ['avatar_256']

    def avatar_256(self, obj):
        request = self.context.get('request', None)

        return '%s/files/%s/%s/%s' % (domain(request), obj._name, obj.id, "avatar_256") if obj.avatar_256 and request else None
