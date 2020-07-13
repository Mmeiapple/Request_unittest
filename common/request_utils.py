import os
import ast
import requests
import jsonpath
import re
from common.get_config import getconfig

class RequestUtils():
    def __init__(self):
        self.hots=getconfig.geturl
        self.headers={'Content-Type': 'application/json'}
        self.seesion=requests.session()
        self.temp_variables={}
    def __get(self,get_infos):
        url=self.hots+get_infos["请求地址"]
        response=self.seesion.get(url=url,
                                  params=ast.literal_eval(get_infos["请求参数"]))
        response.encoding=response.apparent_encoding

        if get_infos["取值方式"]=="json取值":
            #jsonpath.jsonpath(匹配的字典,'jsonpath取值的表达式')
            value=jsonpath.jsonpath(response.json(),get_infos["取值代码"])[0]
            self.temp_variables[ get_infos["传值变量"]]=value
            print("获取token的值为:",self.temp_variables[ get_infos["传值变量"]],'\n')
        elif get_infos["取值方式"]=="正则取值":
            value=re.findall(get_infos["取值代码"],response.text)[0]
            self.temp_variables[get_infos["传值变量"]]=value
            print("获取token的值为:", self.temp_variables[get_infos["传值变量"]], '\n')

        result={'code':'0',
                'response_response':response.reason,
                'response_code':response.status_code,
                'response_header':response.headers,
                'response_body':response.text

                }
        return result

    def __post(self,get_infos):
        url=self.hots+get_infos["请求地址"]
        response=self.seesion.get(url=url,
                                  headers=self.headers,
                                  params=ast.literal_eval(get_infos["请求参数"]),
                                  json=ast.literal_eval(get_infos["请求参数"]))
        response.encoding=response.apparent_encoding

        if get_infos["取值方式"] == "json取值":
            # jsonpath.jsonpath(匹配的字典,'jsonpath取值的表达式')
            value = jsonpath.jsonpath(response.json(), get_infos["取值代码"])[0]
            self.temp_variables[get_infos["传值变量"]] = value
            print("获取token的值为:", self.temp_variables[get_infos["传值变量"]], '\n')
        elif get_infos["取值方式"] == "正则取值":
            value = re.findall(get_infos["取值代码"], response.text)[0]
            self.temp_variables[get_infos["传值变量"]] = value
            print("获取token的值为:", self.temp_variables[get_infos["传值变量"]], '\n')

        result={'code':'0',
                'response_response':response.reason,
                'response_code':response.status_code,
                'response_header':response.headers,
                'response_body':response.text

                }
        return result

    def request(self,step_infos):
        request_type=step_infos["请求方式"]
        if request_type=="get":
            result=self.__get(step_infos)
        elif request_type =='post':
            result=self.__post(step_infos)
        else:
            result={'code':'3',
                    'result':'请求结果不支持'}
        return result
    def request_by_step(self,step_infos):
        for step_info in step_infos:
            temp_result=self.request(step_info)
            if temp_result['code']!=0:
                break
        return temp_result

if __name__=="__main__":
    get_infos1={'请求方式':'get',
               '请求地址':'cgi-bin/token?',
               '请求参数':"{'grant_type':'client_credential','appid':'wx60536c088aee3040','secret':'f214d833f873d8cc1b38255eca0938d9'}",
               "取值方式": "json取值",
               '取值代码': '$.access_token',
               '传值变量':  None
               }
    get_infos2={'请求方式':'get',
               '请求地址':'cgi-bin/token?',
               '请求参数':"{'grant_type':'client_credential','appid':'wx60536c088aee3040','secret':'f214d833f873d8cc1b38255eca0938d9'}",
               "取值方式": "正则取值",
               '取值代码': '"access_token":"(.+?)",',
               '传值变量':  None
               }
    print(RequestUtils().request(get_infos2))



