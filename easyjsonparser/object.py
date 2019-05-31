from .value import EasyJSONValue
from .helper import keyValIterator, EASY_NONEHELPER
from .objectinstance import EasyJSONObjectInstance


class EasyJSONObject(EasyJSONValue):
    _instance_obj_computed = False
    _instance_type = None

    def _get_schema(self):
        schema = []
        for key, item in self.__class__.__dict__.items():
            if key.startswith("__"):
                continue
            elif not isinstance(item, EasyJSONValue):
                continue

            child_schema = item.get_schema() if item is not None else None
            schema.append({"key": key, "value": child_schema})

        return schema

    @property
    def instance_object_type(self):
        if self.__class__._instance_obj_computed:
            return self.__class__._instance_type

        self.__class__._instance_type = self._instance_object_type()
        self.__class__._instance_obj_computed = True
        return self.__class__._instance_type

    def _instance_object_type(self):
        schema = self.get_schema()
        attrs = {key: None for key, value in keyValIterator(schema) }
        attrs.update({"__easy_keys__": attrs.keys()})

        class_name = f"{self.__class__.__name__}EasyInstance"
        result = type(class_name,
                      (EasyJSONObjectInstance, ),
                      attrs)
        return result

    def validate(self, srcval):
        if not isinstance(srcval, dict):
            return False, 'Invalid object'

        schema = self.get_schema()
        for key, valschema in keyValIterator(schema):
            if key not in srcval:
                if valschema.optional:
                    continue
                # If the field is not optional but a default value
                # has been set, validate the field
                elif valschema.default is not EASY_NONEHELPER:
                    continue

                return False, f'{key} does not exist'

            validated, error = valschema.validate(srcval.get(key))
            if not validated:
                return False, f'Error during "{key}"\'s value validation: {error}'

        return True, None

    def compute(self, srcval):
        def schema_value(schema, key):
            if key not in srcval:
                return schema.default if schema.default is not EASY_NONEHELPER else None
            return schema.compute(srcval.get(key))

        constructor_dict = {key: schema_value(valschema, key)
                            for (key, valschema) in keyValIterator(self.get_schema())}
        return self.instance_object_type(**constructor_dict)
