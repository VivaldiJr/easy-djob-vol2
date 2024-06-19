class PaginatorSerializer:
    def __init__(self, request, table, query_search, serializer, page, take, *args, **kwargs):
        self.request = request
        self.table = table
        self.query_search = query_search
        self.serializer = serializer
        self.page = int(page) if page else 1
        self.take = int(take) if take else 10
        self.user = kwargs.get("user", None)
        self.order = kwargs.get('order', 'id desc')

    def query(self, all=False):
        if all:
            if self.user:
                return self.request.env[self.table].with_user(self.user).search(self.query_search, order=self.order)
            return self.request.env[self.table].sudo().search(self.query_search, order=self.order)
        offset = 0 if self.page <= 1 else (self.page - 1) * self.take
        if self.user:
            return self.request.env[self.table].with_user(self.user).search(self.query_search, order=self.order, offset=offset, limit=self.take)
        return self.request.env[self.table].sudo().search(self.query_search, order=self.order, offset=offset, limit=self.take)

    def query_serializer(self, all=False):
        query = self.query(all=all)
        return self.serializer(data=query, many=True, context={"request": self.request}).serializer()

    def meta(self):
        total = self.query(all=True)
        offset = 0 if self.page <= 1 else (self.page - 1) * self.take
        return {
            "total": len(total),
            "current": {
                "take": self.take,
                "page": self.page
            },
            "next": {
                "take": self.take,
                "page": self.page + 1,
            } if len(total) > offset + self.take else None,
            "back": {
                "take": self.take,
                "page": self.page - 1
            } if self.page > 1 and len(total) > 0 else None
        }


class DlinkSerializer(object):

    def __init__(self, data=None, *args, **kwargs):
        self.context = kwargs.get('context', {})

        self.data = data
        self.many = kwargs.get('many', False)
        self.meta = getattr(self, 'Meta', None)

        if not self.meta:
            raise ValueError("class Meta required")
        self.bytes = self.meta.__dict__.get('bytes', [])
        if not self.meta.__dict__.get('model', None):
            raise ValueError("model required on  Meta ")
        if not self.meta.__dict__.get('fields', None):
            raise ValueError("fields required on  Meta , can use __all__ or ['fielname']")

    def serializer(self):

        many = getattr(self, 'many', None)
        self.meta = getattr(self, 'Meta', None)
        if not self.data:
            if many:
                return []
            return None

        data_name = type(self.data).__dict__.get('_name', None)
        model_name = self.meta.model.__dict__.get('_name', None)
        if data_name != model_name or (data_name is None or model_name is None):
            raise ValueError("Query no support for this serializer")

        nif = self.meta.__dict__.get('nif', [])
        exclude = self.meta.__dict__.get('exclude', [])
        if not self.data:
            return None

        value_dict = {}
        value_array = []
        fields = self.meta.fields

        if many:
            objects_to_iterate = self.data
            if fields == '__all__':
                fields = self.data[0]._fields
        else:
            objects_to_iterate = [self.data]
            if fields == '__all__':
                fields = self.data._fields

        for obj in objects_to_iterate:
            value_dict = {}

            for f in fields:
                if f not in exclude:
                    try:
                        className = type(getattr(obj, f)).__dict__.get('_name', None)
                        sclass = getattr(self, f, None)

                        if sclass:
                            if not className:
                                raise ValueError("This field can't serialize")
                            sclass.data = getattr(obj, f)
                            sclass.context = getattr(self, 'context', {})
                            sclass.many = getattr(sclass, 'many', False)
                            sclass.bytes = getattr(sclass, 'bytes', [])
                            value_dict[f] = sclass.serializer()
                        else:

                            if className:

                                type_relation = str(type(obj._fields.get(f, None)))
                                if type_relation == "<class 'odoo.fields.Many2one'>":

                                    if len(getattr(obj, f)) == 1:
                                        value_dict[f] = getattr(obj, f).id
                                    else:
                                        value_dict[f] = None

                                else:

                                    value_dict[f] = [obj.id for obj in getattr(obj, f)]
                            else:
                                typeName = str(type(getattr(obj, f))).split("<class '")[1].split("'>")[0]

                                if typeName == 'bool' and getattr(obj, f) == False and f not in nif:
                                    value_dict[f] = None

                                else:
                                    if typeName == 'bytes':
                                        value_dict[f] = getattr(obj, f).decode('utf-8')
                                    elif typeName == 'datetime.date':
                                        value_dict[f] = "{} {}".format(getattr(obj, f), "00:00:00")

                                    elif typeName == 'datetime.datetime':
                                        value_dict[f] = "{}".format(getattr(obj, f))
                                    else:
                                        value_dict[f] = getattr(obj, f)
                    except Exception as e:
                        print(">>>>>>>>>>> {}".format(e))

            functions = self.meta.__dict__.get('functions', [])
            for fun in functions:
                value_dict[fun] = getattr(self, fun)(obj)

            value_array.append(value_dict)

        if many:
            return value_array
        return value_dict
