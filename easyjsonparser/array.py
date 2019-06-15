from .value import _Value, _raise_bad_value_error
from .helper import JSONArrayMetaclass


class Array(_Value, metaclass=JSONArrayMetaclass):
    __schema__ = None

    def __init__(self, schema=None, minsize=0, maxsize=-1, *args, **kwargs):
        if not isinstance(schema, _Value):
            _raise_bad_value_error(schema, "Invalid schema supplied for EasyJSONArray")

        self._schema = schema
        self._minsize = minsize
        self._maxsize = maxsize

        super().__init__(*args, **kwargs)

    @property
    def schema(self):
        return self.__schema__ if self.__schema__ is not None else self._schema

    def compute_instance_type(self):
        result = type("ArrayInstance", (_ArrayInstance, ), {
            "__default__": self.default,
            "__optional__": self.is_optional,
            "__schema__": self.schema
        })
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


class _ArrayInstance(object):
    __minsize__ = None
    __maxsize__ = None
    __schema__ = None

    def __init__(self, *values):
        self.__values = None
        self.value = values

    def __repr__(self):
        return "<JSON {classname}: {schema}>".format(classname=self.__class__.__name__,
                                                     schema=self.__schema__)

    def __str__(self):
        return "<JSON {classname}: [{content}]>".format(classname=self.__class__.__name__,
                                                        content=", ".join(str(val) for val in self.value))

    def check_and_sanitize_input(self, value):
        if not isinstance(value, (list, tuple)):
            _raise_bad_value_error(value, "List or tuple expected")
        # elif len(values) < self.__class__.__minsize__:
        #     raise RuntimeError("Error during array assignment: "
        #                        "expected a minimum size of {}".format(self.__class__.__minsize__))
        # elif len(values) > self.__class__.__maxsize__:
        #     raise RuntimeError("Error during array assignment: "
        #                        "expected a maximum size of {}".format(self.__class__.__maxsize__))
        result = []
        for val in value:
            entry = self.__schema__()
            entry.fill(val)
            result.append(entry)
        return result

    @property
    def value(self):
        return self.__values

    @value.setter
    def value(self, value):
        self.__values = self.check_and_sanitize_input(value)


    def fill(self, value):
        self.value = value
        
    def to_json(self):
        return "[{}]".format(", ".join(array_val.to_json() for array_val in self.value))
