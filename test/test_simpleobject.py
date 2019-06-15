import unittest
from easyjsonparser.document import JSONObjectDocument
from easyjsonparser.object import _ObjectInstance
from easyjsonparser import Integer, String


class SimpleObject(JSONObjectDocument):
    int_attr1 = Integer(optional=True, default=0)
    int_attr2 = Integer()
    str_attr1 = String(optional=True, default="<Default>")
    str_attr2 = String()


class TestSimpleObject(unittest.TestCase):
    test_string = """
        {
            "int_attr2": 0,
            "str_attr2": "string"
        }
    """

    def test_loads(self):
        obj = SimpleObject.loads(self.test_string)
        self.assertTrue(isinstance(obj, _ObjectInstance))
        self.assertEqual(obj.int_attr2, 0)
        self.assertEqual(obj.str_attr2, "string")

    def test_find(self):
        obj = SimpleObject.loads(self.test_string)
        result = obj.find(String)
        self.assertEqual(result, "string")


if __name__ == "__main__":
    unittest.main()
