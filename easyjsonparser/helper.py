import inspect


def _valid_entry(key, val):
    return (not (key.startswith("__") and key.endswith("__"))) \
           and not inspect.isclass(val) \
           and not inspect.ismethod(val)


def _get_value_if_primitive(schema):
    if not isinstance(schema, NotPrimitiveInstance):
        return schema.value
    return schema


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
                "__schema__": attrs.pop("schema")
            })
        return super().__new__(cls, name, bases, attrs)


class NotPrimitiveInstance(object):
    pass


class PrivateEasyNoneHelper(NotPrimitiveInstance):
    def __repr__(self):
        return '<Empty value>'

    def __str__(self):
        return self.__repr__()


_helperEmpty = None


def Empty():
    """
    Returns a comprehensible empty value. The idea behind this is that None is
    an acceptable value for null so we need something different
    """
    global _helperEmpty
    if _helperEmpty is None:
        _helperEmpty = PrivateEasyNoneHelper()
    return _helperEmpty
