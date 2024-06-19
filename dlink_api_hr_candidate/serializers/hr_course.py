from odoo.addons.hr_candidate.models.hr_candidate import HrCourse
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrCourseSerializer(DlinkSerializer):
    class Meta:
        model = HrCourse
        fields = ['id', 'name']
