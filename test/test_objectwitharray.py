from easyjsonparser import Array, String
from easyjsonparser.document import JSONObjectDocument

class TestObjectWithArray(JSONObjectDocument):
    array = Array(String(default="Default"))
    array2 = Array(String(default="Default2"))

obj = TestObjectWithArray.create()
obj.array = ["Test", "Test1"]
obj.array2 = ["Test3", "Test4"]

obj2 = TestObjectWithArray.create()
obj2.array = ["Test5"]

print(obj)
print(obj2)


obj3 = TestObjectWithArray.loads("""
{
    "array": ["11", "33"],
    "array2": ["Yesy", "1"]
}
""")
print(obj3.to_json())