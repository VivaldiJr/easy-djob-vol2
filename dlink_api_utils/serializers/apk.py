from odoo.addons.dlink_api_utils import DlinkSerializer
from odoo.addons.dlink_api_utils.models.apk import AppUpdate
from odoo.addons.dlink_api_utils.utils.domain import domain


class ApkUpdateSerializer(DlinkSerializer):
    class Meta:
        model = AppUpdate
        fields = '__all__'
        exclude = ['__last_update', 'display_name', 'create_uid', 'create_date', 'write_uid', 'write_date', 'file']
        nif = ['name', 'version', 'file_url', 'datetime']
        functions = ['file_url']

    def file_url(self, obj):
        request = self.context.get('request', None)
        return '%s/files/%s/%s/%s' % (domain(request), obj._name, obj.id, "file") if obj.file else None
