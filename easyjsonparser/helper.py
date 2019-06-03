import inspect

class PrivateEasyNoneHelper:
    def __repr__(self):
        return '<Empty value>'

    def __str__(self):
        return self.__repr__()


def _valid_entry(key, val):
    return (not (key.startswith("__") and key.endswith("__"))) \
           and not inspect.isclass(val) \
           and not inspect.ismethod(val)


class JSONObjectMetaclass(type):
    @staticmethod
    def add_property_name(key, schema):
        schema.__property_name__ = key
        return schema

    def __new__(cls, name, bases, attrs):
        if name == "Object" or name == "object":
            return super().__new__(cls, name, bases, attrs)

        if "__attributes__" not in attrs:
            attrs.update({
                "__attributes__": {key: JSONObjectMetaclass.add_property_name(key, schema)
                                   for key, schema in attrs.items() if _valid_entry(key, schema)}
            })
        result_type = super().__new__(cls, name, bases, attrs)
        return result_type


class JSONArrayMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == "Array" or name == "object":
            return super().__new__(cls, name, bases, attrs)

        if "schema" not in attrs:
            raise RuntimeError("No schema was specified for the JSON array document")

        if "__schema__" not in attrs:
            attrs.update({
                "__schema__": attrs.get("schema")
            })
        return super().__new__(cls, name, bases, attrs)

Empty = PrivateEasyNoneHelper()