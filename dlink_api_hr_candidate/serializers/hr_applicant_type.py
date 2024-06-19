from odoo.addons.hr_recruitment.models.hr_recruitment import RecruitmentDegree
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrApplicantTypeSerializer(DlinkSerializer):
    class Meta:
        model = RecruitmentDegree
        fields = ['id', 'name']
