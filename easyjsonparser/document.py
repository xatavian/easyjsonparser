from .object import EasyJSONObject
from .array import EasyJSONArray


class EasyJSONDocument(object):
    @staticmethod
    def parse_json(srcstr):
        import json
        try:
            return json.loads(srcstr)
        except json.JSONDecodeError as e:
            print(e)
            raise RuntimeError("The supplied document is not a valid JSON document")

    @staticmethod
    def validate_str(SrcDocument, srcstr):
        if not issubclass(SrcDocument, EasyJSONObject) and not issubclass(SrcDocument, EasyJSONArray):
            raise RuntimeError("Can only validate against JSON objects or arrays")
        elif not isinstance(srcstr, str):
            raise RuntimeError("validate_str only validates strings")

        return EasyJSONDocument.validate(SrcDocument,
                                         EasyJSONDocument.parse_json(srcstr))

    @staticmethod
    def validate(SrcDocument, src):
        if not issubclass(SrcDocument, EasyJSONObject) and not issubclass(SrcDocument, EasyJSONArray):
            raise RuntimeError("Can only validate against JSON objects or arrays")
        return SrcDocument().validate(src)

    @staticmethod
    def compute_str(SrcDocument, srcstr):
        if not issubclass(SrcDocument, EasyJSONObject) and not issubclass(SrcDocument, EasyJSONArray):
            raise RuntimeError("EasyJSONDocument computations are only available for "
                               "JSON objects or array")
        elif not isinstance(srcstr, str):
            raise RuntimeError("EasyJSONDocument.compute_str only handles string inputs")

        jsondoc = EasyJSONDocument.parse_json(srcstr)

        doc = SrcDocument()
        success, error = doc.validate(jsondoc)
        if not success:
            raise RuntimeError("EasyJSONDocument.compute failed because the supplied "
                               "document is not valid.\n"
                               f"Error: {error}")
        return doc.compute(jsondoc)

    @staticmethod
    def compute(SrcDocument, src):
        if not issubclass(SrcDocument, EasyJSONObject) and not issubclass(SrcDocument, EasyJSONArray):
            raise RuntimeError("EasyJSONDocument computations are only available for "
                               "JSON objects or array")
        doc = SrcDocument()
        success, error = doc.validate(src)
        if not success:
            raise RuntimeError("EasyJSONDocument.compute failed because the supplied "
                               "document is not valid.\n"
                               f"Error: {error}")
        return doc.compute(src)
