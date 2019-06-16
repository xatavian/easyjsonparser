from .value import _Value, _ValueInstance, _raise_bad_value_error
from .helper import JSONObjectMetaclass, Empty, NotPrimitiveInstance, \
                    _get_value_if_primitive


class Object(_Value, metaclass=JSONObjectMetaclass):
    """
    Schema-class representing a JSON object.
    Its metaclass automatically computes its list of attributes accessible
    both in the class and its instances through Object.attributes().
    """
    __attributes__ = None

    def compute_instance_attributes(self):
        result = {
            attr_name: _ObjectInstance._accesser(attr_name, attr_schema)
            for attr_name, attr_schema in self.attributes().items()
        }
        result.update(
            {"__attributes__": [key for key in self.attributes()]}
        )
        result.update(self._default_value_instance_params())
        return result

    def compute_instance_type(self):
        class_name = "{classname}Instance".format(
            classname=self.__class__.__name__)
        result = type(class_name,
                      (_ObjectInstance, ),
                      self.compute_instance_attributes())
        return result

    def check_params(self):
        if not isinstance(self.default, dict):
            return super().check_params()

        for key, attr in self.default.items():
            if key not in self.__attributes__:
                raise RuntimeError("Bad default value: {key} is not a "
                                   "registered attribute of {classname}"
                                   .format(key=key,
                                           classname=self.__class__.__name__))

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


class _ObjectInstance(_ValueInstance, NotPrimitiveInstance):
    """
    Base-class of every class that represent a JSON object instance.
    """
    __attributes__ = None

    @staticmethod
    def _accesser(name, schema):
        @property
        def accessmethod(self):
            if name not in self.__internal_dict:
                self.__internal_dict[name] = schema()
            return self.__internal_dict[name]

        @accessmethod.setter
        def accessmethod(self, val):
            if name not in self.__internal_dict:
                self.__internal_dict[name] = schema()
            self.__internal_dict[name].value = val

        return accessmethod

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.__internal_dict = {}

    def __repr__(self):
        return "<JSON {classname}, attributes number: {attrs_num}>".format(
            classname=self.__class__.__name__,
            attrs_num=len(self.__attributes__)
            if self.__attributes__ is not None else 0)

    def __str__(self):
        ctnt = ('"{name}": {value}'.format(name=objname,
                                           value=getattr(self, objname))
                for objname in self.__attributes__)
        return "<JSON {classname}: {{{content}}}>".format(
            classname=self.__class__.__name__,
            content=', '.join(ctnt)
        )

    def compute_to_json(self):
        if self.__attributes__ is None:
            return "{}"

        def attr_to_print(attr):
            # entry = getattr(self, attr)
            # if entry.value is Empty() and entry.is_optional:
            #     return False
            return True

        def getattr_json(self, attr):
            obj = getattr(self, attr)
            if isinstance(obj, NotPrimitiveInstance):
                return obj.to_json()
            elif isinstance(obj, str):
                return '"{}"'.format(obj)
            return obj

        ctnt = ('"{attr}": {value}'.format(attr=attr,
                                           value=getattr_json(self, attr))
                for attr in self.__attributes__ if attr_to_print(attr))
        return "{{{content}}}".format(content=", ".join(ctnt))

    def __getattribute__(self, item):
        builtin_getattr = object.__getattribute__
        if item not in builtin_getattr(self, "__attributes__"):
            return builtin_getattr(self, item)

        return _get_value_if_primitive(builtin_getattr(self, item))

    def __setattr__(self, item, value):
        if item not in self.__attributes__:
            return object.__setattr__(self, item, value)

        attr_schema = object.__getattribute__(self, item)
        attr_schema.value = value

    def check_and_sanitize_input(self, value):
        if not isinstance(value, dict):
            _raise_bad_value_error(
                value,
                self.__property_name__,
                "Dict type expected"
            )

        for key in value:
            if key not in self.__attributes__:
                _raise_bad_value_error(
                    value,
                    self.__property_name__,
                    'Unexpected key {key} for object-type "{classname}"'
                    .format(key=key, classname=self.__class__.__name__)
                )
        return value

    @property
    def value(self):
        return {attr: getattr(self, attr) for attr in self.__attributes__}

    @value.setter
    def value(self, newval):
        src = self.check_and_sanitize_input(newval)
        if src is Empty():
            for key in self.__attributes__:
                setattr(self, key, Empty())
        else:
            for key, value in src.items():
                setattr(self, key, value)

    def find(self, targetschema):
        for attr in self.__schema__.attributes():
            child_schema = getattr(self.__schema__, attr)
            if isinstance(child_schema, targetschema):
                val = getattr(self, attr)
                if val is not Empty():
                    return val
            elif isinstance(child_schema, NotPrimitiveInstance):
                child_val = getattr(self, attr).find(targetschema)
                if child_val is not None:
                    return child_val
        return Empty()

    def find_all(self, targetschema):
        result = []
        for attr in self.__schema__.attributes():
            child_schema = getattr(self.__schema__, attr)
            if isinstance(child_schema, targetschema):
                result.append(getattr(self, attr))
            elif isinstance(child_schema, NotPrimitiveInstance):
                result.extend(getattr(self, attr).findAll(targetschema))
        return result
