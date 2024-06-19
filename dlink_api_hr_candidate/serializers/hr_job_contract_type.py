from odoo.addons.hr.models.hr_contract_type import ContractType

from odoo.addons.dlink_api_utils import DlinkSerializer


class HrJobContractTypeSerializer(DlinkSerializer):
    class Meta:
        model = ContractType
        fields = ['id', 'name']
