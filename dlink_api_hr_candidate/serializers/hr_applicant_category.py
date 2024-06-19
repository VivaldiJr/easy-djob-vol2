from odoo.addons.hr_recruitment.models.hr_recruitment import ApplicantCategory
from odoo.addons.dlink_api_utils import DlinkSerializer


class HrApplicantCategorySerializer(DlinkSerializer):
    class Meta:
        model = ApplicantCategory
        fields = ['id', 'name']
