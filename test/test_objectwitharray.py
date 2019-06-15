from easyjsonparser import Array, String
from easyjsonparser.document import JSONObjectDocument
import unittest


class ObjectWithArray(JSONObjectDocument):
    array = Array(String())
    array2 = Array(String())


class TestObjectWithArray(unittest.TestCase):
    test_string = """
    {
        "array": ["Pilot", "Co-pilot"],
        "array2": ["Orange", "Banana"]
    }
    """

    def test_loads(self):
        obj = ObjectWithArray.loads(self.test_string)
        self.assertEqual(len(obj.array), 2)
        self.assertEqual(obj.array2[0], "Orange")

    def test_mutating(self):
        obj = ObjectWithArray.loads(self.test_string)
        obj.array = ["NY->Paris", "NY->SF"]
        obj.array2[1] = "Error-string"

        self.assertFalse(isinstance(obj.array, list))
        self.assertEqual(obj.array2[1], "Error-string")
