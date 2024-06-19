from odoo.addons.dlink_api_utils.entiroment import URL_API_BASE

base_api_auth = '{}auth'.format(URL_API_BASE)

tokenAuth_endpoint = '{}/signIn'.format(base_api_auth)
tokenRemove_endpoint = '{}/logOut'.format(base_api_auth)
tokenRefresh_endpoint = '{}/refresh'.format(base_api_auth)
tokenVerify_endpoint = '{}/verify'.format(base_api_auth)
changePassword_endpoint = '{}/password/change'.format(base_api_auth)
timezone_endpoint = '{}/tz'.format(base_api_auth)
language_endpoint = '{}/lang'.format(base_api_auth)
