import json


def dealRes(res):
    res=res[0:len(res)-3]
    res=json.loads(res)
    return res

res=dealRes('{"method":"upload","data":[{"Name":"R1","Value":"038"},{"Name":"E1","Value":"33"},{"Name":"R2","Value":"33"},{"Name":"E2","Value":"33"},{"Name":"E3","Value":" 998"}]}&^!');
print(res)
data=res['data']
for i in data:
    print(i)

print()