from ..models.access_token import APIAccessToken, EXPIRE_TOKEN
from ..serializers.user import UserSerializer
from odoo.addons.dlink_api_utils import  DlinkSerializer


class TokenSerializer(DlinkSerializer):
    user_id = UserSerializer()

    class Meta:
        model = APIAccessToken
        fields = ['token', 'refresh', 'user_id'] if EXPIRE_TOKEN else ['token', 'user_id']
