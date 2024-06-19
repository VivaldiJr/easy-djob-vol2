from odoo.http import request
from .const import DATETIME_FORMAT, DATE_FORMAT, TYPES
from .field_validator import ValidateFields


class FieldRequired:
    def __str__(self):
        return "{} -> {}".format(self.key, self.type)

    # If you pass choices = [] , the field required list of type defined
    def __init__(self, key, type: TYPES, relation: str = None, param: str = 'id', required=True, choices=None, fields=None or []):
        if type not in TYPES:
            raise ValueError(f"Type {type} of data no valid")

        if type == 'dict' and not fields:
            raise ValueError("Type dict required more fields")
        if fields and not type == 'dict':
            raise ValueError("Only accept fields in type dict")
        for f in fields:
            if not isinstance(f, FieldRequired):
                raise ValueError("{} not is Instance of FieldRequired".format(f))
        self.key = key
        self.type = type
        self.param = param
        self.choices = choices
        self.relation = relation
        self.required = required
        self.fields = [] if fields is None else fields

    def validate(self, data, isHttp=False):
        response = []

        typeName, value = self._type_name_special_valid(data)
        if self.choices == [] and value is not None:
            all_valid = True
            if typeName == 'list':
                for d in data.get(self.key, []):
                    if self.fields and self.type == 'dict':
                        for f in self.fields:
                            if f.validate(d, isHttp):
                                all_valid = False
                    else:
                        t, v = self._type_name_special_valid({self.key: d})
                        if not t == self.type:
                            all_valid = False
                if not all_valid:
                    response.append(self.error_json(data, isHttp))
                return response
            else:
                response.append(self.error_json(data, isHttp=isHttp))
                return response
        error_relation = False if value is not None else True
        error_choices = False if value is not None else True
        error_dict = False if value is not None else True

        if self.relation and value:
            query_search = [(self.param, "=", value)]
            try:
                object = request.env[self.relation].sudo().search(query_search)
                if not object:
                    error_relation = True
            except:
                error_relation = True

        if self.choices and value:
            if value not in self.choices:
                error_choices = True

        if self.type == 'dict':
            for fi in self.fields:
                if fi.validate(data.get(self.key, {}), isHttp=isHttp):
                    error_dict = True

        if value is None or typeName != self.type or error_relation or error_choices or error_dict:
            if self.required:
                response.append(self.error_json(data, isHttp=isHttp))
            elif value is not None:
                response.append(self.error_json(data, isHttp=isHttp))
        return response

    def error_json(self, data, isHttp=False):
        info = self.type
        if self.type == 'date':
            info = "{} {}".format(self.type, DATE_FORMAT)

        if self.type == 'datetime':
            info = "{} {}".format(self.type, DATETIME_FORMAT)

        map = {"key": self.key, "type": info}

        if self.type == 'dict':
            array_errors = []
            for f in self.fields:
                array_errors.append(f.error_json(data.get(f.key, {}), isHttp=isHttp))
            map['dict'] = array_errors
        if self.relation:
            map['relation'] = {
                "model": self.relation,
                "param": self.param
            }
        if self.choices:
            map['choices'] = self.choices

        return map

    def _type_name_special_valid(self, data) -> []:
        if not ValidateFields.isMap(data):
            return ["NoneType", None]
        _type = type(data.get(self.key, None))

        typeName = str(_type).split("<class '")[1].split("'>")[0]

        if typeName == 'NoneType':
            return [typeName, None]

        if self.type == 'binary' and typeName == 'str':
            typeName = 'binary' if ValidateFields.isBase64(data.get(self.key, None)) else 'str'
        if self.type == 'float' and typeName == 'int':
            typeName = 'float'
        if self.type == 'file' and typeName == 'werkzeug.datastructures.FileStorage':
            typeName = 'file'

        if self.type == 'date' and typeName == 'str':
            d = ValidateFields.isDate(data.get(self.key, None))
            if d:
                typeName = 'date'
                return [typeName, d]
        if self.type == 'datetime' and typeName == 'str':
            dt = ValidateFields.isDateTime(data.get(self.key, None))
            if dt:
                typeName = 'datetime'
                return [typeName, dt]

        if self.type == 'dict' and typeName == 'str':
            typeName = 'dict' if ValidateFields.isMap(data.get(self.key, None)) else 'str'

        if self.type == 'email' and typeName == 'str':
            typeName = 'email' if ValidateFields.isEmail(data.get(self.key, None)) else 'str'

        if self.type == 'url' and typeName == 'str':
            typeName = 'url' if ValidateFields.isUrl(data.get(self.key, None)) else 'str'

        return [typeName, data.get(self.key, None)]
