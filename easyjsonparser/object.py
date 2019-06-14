from .value import _Value, _raise_bad_value_error
from .helper import JSONObjectMetaclass, Empty


class Object(_Value, metaclass=JSONObjectMetaclass):
    __attributes__ = None

    def compute_instance_attributes(self):
        result = {attr_name: attr_schema() for attr_name, attr_schema in self.attributes().items()}
        result.update({"__attributes__": [key for key, val in self.attributes().items()]})
        result.update(self._default_value_instance_params())
        return result

    def compute_instance_type(self):
        class_name = "{classname}Instance".format(classname=self.__class__.__name__)
        result = type(class_name,
                      (_ObjectInstance, ),
                      self.compute_instance_attributes())
        return result

    def check_params(self):
        if not isinstance(self.default, dict):
            return super().check_params()

        for key, attr in self.default.items():
            if key not in self.__attributes__:
                raise RuntimeError("Bad default value: {key} is not a registered "
                                   "attribute of {classname}".format(key=key, classname=self.__class__.__name__))

    @classmethod
    def attributes(cls):
        return cls.__attributes__

    # def validate(self, srcval):
    #     if not isinstance(srcval, dict):
    #         return False, 'Invalid object'
    #
    #     schema = self.get_schema()
    #     for key, valschema in keyValIterator(schema):
    #         if key not in srcval:
    #             if valschema.is_optional:
    #                 continue
    #             # If the field is not optional but a default value
    #             # has been set, validate the field
    #             elif valschema.default is not EASY_NONEHELPER:
    #                 continue
    #
    #             return False, f'{key} does not exist'
    #
    #         validated, error = valschema.validate(srcval.get(key))
    #         if not validated:
    #             return False, f'Error during "{key}"\'s value validation: {error}'
    #
    #     return True, None
    #
    # def compute(self, srcval):
    #     def schema_value(schema, key):
    #         if key not in srcval:
    #             return schema.default if schema.default is not EASY_NONEHELPER else None
    #         return schema.compute(srcval.get(key))
    #
    #     constructor_dict = {key: schema_value(valschema, key)
    #                         for (key, valschema) in keyValIterator(self.get_schema())}
    #     return self.instance_type(**constructor_dict)


class _ObjectInstance(object):
    __attributes__ = None
    __property_name__ = None
    __default__ = Empty
    __optional__ = False

    def __init__(self, **kwargs):
        print("Fill", self.__class__.__name__)
        for key, val in kwargs.items():
            if key not in self.__attributes__:
                raise RuntimeError("Error during object instantiation: "
                                   'invalid keyword "{key}" supplied. '
                                   'List of valid attributes: {attributes}'.format(key=key,
                                                                                   attributes=self.__attributes__))
            setattr(self, key, val)

    def __repr__(self):
        return "<JSON {classname}, attributes number: {attrs_num}>".format(
            classname=self.__class__.__name__,
            attrs_num=len(self.__attributes__) if self.__attributes__ is not None else 0
        )

    def __str__(self):
        return "<JSON {classname}: {{{content}}}>".format(
            classname=self.__class__.__name__,
            content=', '.join('"{name}": {value}'.format(name=objname, value=getattr(self, objname))
                              for objname in self.__attributes__)
        )

    def to_json(self):
        if self.__attributes__ is None:
            return "{}"

        def attr_to_print(attr):
            entry = getattr(self, attr)
            if entry.value is Empty and entry.is_optional:
                return False
            return True

        return "{{{content}}}".format(
            content=", ".join('"{attr}": {value}'.format(attr=attr, value=getattr(self, attr).to_json())
                              for attr in self.__attributes__ if attr_to_print(attr))
        )

    def __getattr__(self, item):
        if item in self.__attributes__:
            return getattr(self, item).value
        return getattr(self, item)

    def __setattr__(self, key, value):
        if key in self.__attributes__:
            getattr(self, key).value = value
        else:
            super().__setattr__(key, value)

    def fill(self, src):
        if not isinstance(src, dict):
            _raise_bad_value_error(src, self.__property_name__, "Dict type expected")

        for key, value in src.items():
            if key not in self.__attributes__:
                _raise_bad_value_error(src,
                                       self.__property_name__,
                                       'Unexpected key {key} for object-type '
                                       '"{classname}"'.format(key=key, classname=self.__class__.__name__))
            getattr(self, key).fill(value)

    @property
    def value(self):
        return {attr: getattr(self, attr) for attr in self.__attributes__}

    @value.setter
    def value(self, newval):
        self.fill(newval)



