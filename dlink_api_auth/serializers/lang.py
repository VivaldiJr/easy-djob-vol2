from odoo.addons.base.models.res_lang import Lang
from odoo.addons.dlink_api_utils import DlinkSerializer


class LanguageSerializer(DlinkSerializer):
    class Meta:
        model = Lang
        fields = ['id', 'code', 'name']
