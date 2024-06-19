from odoo.addons.dlink_api_auth.serializers.user import UserSerializer
from odoo.addons.dlink_api_hr_candidate.serializers.hr_applicant import HrApplicantSerializer
from odoo.addons.mail.models.mail_activity import MailActivity
from odoo.addons.dlink_api_utils import DlinkSerializer


class MailActivitySerializer(DlinkSerializer):
    user_id = UserSerializer()

    class Meta:
        model = MailActivity
        fields = ['activity_type_id', 'display_name', 'user_id', 'create_date', 'write_date', 'date_deadline']
        functions = ['hr_applicant']

    def hr_applicant(self, obj):
        request = self.context.get('request', None)
        if obj.res_model == "hr.applicant":
            return HrApplicantSerializer(data=request.env['hr.applicant'].sudo().search([("id", "=", obj.res_id)]),
                                         context={"request": request}).serializer()
        return None
