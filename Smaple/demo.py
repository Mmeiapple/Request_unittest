import jsonpath
import re
# def test(get_infos):


# get_infos={"取值方式":"json",'取值代码':'$.access_token'}
# temp_variable ={}
#
# # if get_infos["取值方式"] == "json取值":
# response={"access_token":"35_LaCmfqXiABALGW","expires_in":7200}
# # value = jsonpath.jsonpath(response.json(), get_infos["取值代码"])[0]
# # temp_variable[get_infos["传值变量"]] = value
#
# value=jsonpath.jsonpath( response, get_infos["取值代码"])[0]
# print(type(value))
#


#单个替换

tempdata={'token':'123456'}

params='{"access_token":${token}}'
print('替换前:%s'%(params))
value=re.findall('\\${\w+}',params)[0]
params=params.replace(value,tempdata.get(value[2:-1]))

print('替换后:%s'%(params))

# 多个替换

tempdata={'token':'123456','age':'12','data':'1997-01-08'}
param2='{"access_token":${token},"age":${age},"data":${data}}'

for values in re.findall('\\${\w+}',param2):
    param2=param2.replace(values,('"%s"'%tempdata.get(values[2:-1])))
print(param2)