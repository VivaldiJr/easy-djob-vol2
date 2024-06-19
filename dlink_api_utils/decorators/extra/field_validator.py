import base64
from datetime import datetime

from .const import DATETIME_FORMAT, DATE_FORMAT


class ValidateFields:
    @staticmethod
    def isBase64(s: str):
        try:
            return base64.b64encode(base64.b64decode(s)).decode('utf-8') == s
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def isMap(s):
        return isinstance(s, dict)

    @staticmethod
    def isDate(s):
        try:
            dateObject = datetime.strptime(s, DATE_FORMAT)
            return dateObject
        except:
            return None

    @staticmethod
    def isDateTime(s):
        try:
            dateObject = datetime.strptime(s, DATETIME_FORMAT)
            return dateObject
        except:
            return None

    @staticmethod
    def isEmail(s):
        import re
        pat = "^[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{2,5}$"
        if re.match(pat, s):
            return True
        return False

    @staticmethod
    def isUrl(s):
        from urllib.parse import urlparse
        result = urlparse(s)
        return result.scheme and result.netloc
