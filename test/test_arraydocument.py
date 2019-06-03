from easyjsonparser.document import JSONArrayDocument
import easyjsonparser as ejp

class TestArray(JSONArrayDocument):
    schema = ejp.String()

class TestArray2(JSONArrayDocument):
    class Object1(ejp.Object):
        attr1 = ejp.Integer()
        attr2 = ejp.String()
    schema = Object1()

array = TestArray.create(["Hello", "Hello2"])
print(array.to_json())

array2 = TestArray2.create({
    "attr1": 1, "attr2": "str"
})
array3 = TestArray2.loads("""
[{"attr1": 14, "attr2": "14"}]
""")
print(array2, array2.to_json())
print(array3, array3.to_json())