from .value import _Value, _ValueInstance, _raise_bad_value_error
from .helper import JSONArrayMetaclass, NotPrimitiveInstance, \
                    _get_value_if_primitive, Empty


class Array(_Value, metaclass=JSONArrayMetaclass):
    """
    Schema-class for JSON arrays.

    Schema parameters:
    -> schema: schema of every element of the array
    -> minsize: required minimum size of the array
    -> maxsize: required maximum size of the array. If the value is negative,
                the behaviour is desactivated

    For other schema parameters, see _Value
    """
    __schema__ = None

    def __init__(self, schema=None, minsize=0, maxsize=-1, *args, **kwargs):
        if not isinstance(schema, _Value):
            _raise_bad_value_error(schema, "Invalid schema supplied for "
                                           "EasyJSONArray")

        self._schema = schema
        self._minsize = minsize
        self._maxsize = maxsize

        super().__init__(*args, **kwargs)

    @property
    def schema(self):
        return self.__schema__ if self.__schema__ is not None else self._schema

    @property
    def minsize(self):
        return self._minsize

    @property
    def maxsize(self):
        return self._maxsize

    def compute_instance_type(self):
        attrs = self._default_value_instance_params()
        attrs.update({
            "__schema__": self.schema,
            "__minsize__": self._minsize,
            "__maxsize__": self._maxsize
        })
        result = type("ArrayInstance",
                      (_ArrayInstance, ),
                      attrs)
        return result

    def check_params(self):
        if not isinstance(self.default, list):
            return super().check_params()
        # elif len(srcval) < self._minsize:
        #     return False, 'Array too small'
        # elif self._maxsize is not None and len(srcval) > self._maxsize:
        #     return False, 'Array too large'

        # for entry in self.default:
        #     success, error = self._schema.validate(entry)
        #     if not success:
        #         return False, f'Error during schema validation: {error}'
        # return True, None


class _ArrayInstance(_ValueInstance, NotPrimitiveInstance):
    __minsize__ = None
    __maxsize__ = None
    __schema__ = None

    def __init__(self, *values):
        self.__values = None
        self.value = values

    def __repr__(self):
        return "<JSON {classname}: {schema}>".format(
            classname=self.__class__.__name__,
            schema=self.__schema__)

    def __str__(self):
        return "<JSON {classname}: [{content}]>".format(
            classname=self.__class__.__name__,
            content=", ".join(str(val) for val in self.value))

    def __getitem__(self, key):
        return _get_value_if_primitive(self.value[key])

    def __setitem__(self, key, value):
        self.__values[key].value = value

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(_get_value_if_primitive(val)
                    for val in self.__values)

    def __contains__(self, value):
        return value in self

    def __reversed__(self):
        return iter(_get_value_if_primitive(val)
                    for val in reversed(self.__values))

    @property
    def value(self):
        return self.__values

    @value.setter
    def value(self, values):
        if isinstance(values, (list, tuple)):
            self.__values = [None] * len(values)
            for i, val in enumerate(values):
                entry = self.__schema__()
                entry.value = val
                self.__values[i] = entry
        elif type(self) is type(values):
            self.__values = [val for val in values]
        else:
            _raise_bad_value_error(values, "List or tuple expected")

    def to_json(self):
        return "[{}]".format(", ".join(array_val.to_json()
                                       for array_val in self.value))

    def find(self, targetschema):
        if isinstance(self.__schema__, targetschema):
            return _get_value_if_primitive(
                self.value[0] if len(self.value) > 0 else Empty()
            )
        elif isinstance(self.__schema__, NotPrimitiveInstance):
            for val in self.value:
                child_val = val.find(targetschema)
                if child_val is not None:
                    return child_val
        return Empty()

    def find_all(self, targetschema):
        if isinstance(self.__schema__, targetschema):
            return self.value
        elif isinstance(self.__schema__, NotPrimitiveInstance):
            result = []
            for val in self.value:
                result.extend(val.find_all(targetschema))
            return []
        return []
