from odoo.addons.base.models.res_currency import Currency
from odoo.addons.dlink_api_utils import DlinkSerializer


class ResCurrencySerializer(DlinkSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name', 'full_name', 'symbol', 'rounding', 'decimal_places']
