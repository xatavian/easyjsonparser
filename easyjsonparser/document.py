from .object import Object, _ObjectInstance
from .array import Array, _ArrayInstance
from .helper import JSONObjectMetaclass, JSONArrayMetaclass
from .value import _raise_bad_value_error
from .value import _Value


class JSONObjectDocument(Object, metaclass=JSONObjectMetaclass):
    @classmethod
    def compute_instance_attributes(cls):
        result = {attr_name: attr_schema() for attr_name, attr_schema in cls.attributes().items()}
        result.update({"__attributes__": [key for key, val in cls.attributes().items()]})
        return result

    @classmethod
    def create(cls, **kwargs):
        class_name = "{classname}Instance".format(classname=cls.__name__)
        result_type = type(class_name,
                           (_ObjectInstance, ),
                           cls.compute_instance_attributes())
        return result_type(**kwargs)

    @classmethod
    def loads(cls, string):
        import json
        try:
            return cls.load(json.loads(string))
        except json.JSONDecodeError as e:
            raise e

    @classmethod
    def load(cls, obj):
        if not isinstance(obj, dict):
            _raise_bad_value_error(obj, "Expected a dict type object")

        result = cls.create(**obj)
        return result


class JSONArrayDocument(Array, metaclass=JSONArrayMetaclass):
    @classmethod
    def create(cls, *values):
        class_name = "{classsname}Instance".format(classsname=cls.__name__)
        result_type = type(class_name,
                           (_ArrayInstance,),
                           {"__schema__": cls.__schema__})
        if len(values) == 1 and isinstance(values[0], (list, tuple)):
            return result_type(*values[0])
        return result_type(*values)

    @classmethod
    def loads(cls, string):
        import json
        try:
            return cls.load(json.loads(string))
        except json.JSONDecodeError as e:
            raise e

    @classmethod
    def load(cls, *values):
        return cls.create(*values)

    @classmethod
    def schema(cls):
        return cls.__schema__

#
# def validate_str(SrcDocument, srcstr):
#     __check_src_type(SrcDocument,
#                      (Object, Array),
#                      "Can only validate against JSON objects or arrays")
#     assert isinstance(srcstr, str)
#     return __validate(SrcDocument, __parse_json(srcstr))
#
#
# def validate(SrcDocument, src):
#     __check_src_type(SrcDocument,
#                      (Object, Array),
#                      "Can only validate against JSON objects or arrays")
#     return __validate(SrcDocument, src)
#
#
# def __validate(SrcDocument, src):
#     assert isinstance(src, (dict, list))
#     return SrcDocument().validate(src)
#
#
# def compute_str(SrcDocument, srcstr):
#     __check_src_type(SrcDocument,
#                      (Object, Array),
#                      "EasyJSONDocument computations are only available for JSON objects or array")
#
#     assert isinstance(srcstr, str)
#     return __compute(SrcDocument, __parse_json(srcstr))
#
#
# def compute(SrcDocument, src):
#     __check_src_type(SrcDocument,
#                      (Object, Array),
#                      "EasyJSONDocument computations are only available for JSON objects or array")
#     return __compute(SrcDocument, src)
#
#
# def __compute(SrcDocument, src):
#     doc = SrcDocument()
#     success, error = doc.validate(src)
#     if not success:
#         raise RuntimeError("EasyJSONDocument.compute failed because the supplied "
#                            "document is not valid.\n"
#                            f"Error: {error}")
#     return doc.compute(src)
#
#
# def __check_src_type(src, types, error_string):
#     for t in types:
#         if issubclass(src, t):
#             return
#     raise RuntimeError(error_string)
#
#
# def __parse_json(srcstr):
#     import json
#     try:
#         return json.loads(srcstr)
#     except json.JSONDecodeError as e:
#         print(e)
#         raise RuntimeError("The supplied document is not a valid JSON document")
