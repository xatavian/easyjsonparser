from easyjsonparser.document import JSONObjectDocument
import easyjsonparser as ejp


class SimpleObject(JSONObjectDocument):
    int_attr1 = ejp.Integer(optional=True, default=0)
    int_attr2 = ejp.Integer()
    str_attr1 = ejp.String(optional=True, default="<Default>")
    str_attr2 = ejp.String()


obj = SimpleObject.loads("""
{
    "int_attr2": 0,
    "str_attr2": "string" 
}
""")

print(obj)
print(obj.to_json())