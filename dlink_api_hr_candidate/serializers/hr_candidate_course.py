from odoo.addons.dlink_api_hr_candidate.serializers.hr_course import HrCourseSerializer
from odoo.addons.hr_candidate.models.hr_candidate import HrCandidateCourse
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrCandidateCourseSerializer(DlinkSerializer):
    course_name = HrCourseSerializer()

    class Meta:
        model = HrCandidateCourse
        fields = ['id', 'candidate_id', 'course_name', 'start_date', 'end_date', 'description']
