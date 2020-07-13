import os
import ast
import requests
import jsonpath
import re
import random
from common.get_config import getconfig

class RequestUtils():
    def __init__(self):
        self.hots='https://api.weixin.qq.com'
        self.headers={'Content-Type': 'application/json'}
        self.seesion=requests.session()
        self.temp_variables={}

    def __get(self,get_infos):
        url=self.hots+get_infos["请求地址"]
        response=self.seesion.get(url=url,
                                  params=ast.literal_eval(get_infos["请求参数(get)"]))

        response.encoding=response.apparent_encoding

        if get_infos["取值方式"]=="json取值":
            #jsonpath.jsonpath(匹配的字典,'jsonpath取值的表达式')
            value = jsonpath.jsonpath( response.json(),get_infos["取值代码"] )[0]
            self.temp_variables[ get_infos["传值变量"] ] = value
            # print("获取token的值为:",self.temp_variables[ get_infos["传值变量"]],'\n')
        elif get_infos["取值方式"]=="正则取值":
            value=re.findall(get_infos["取值方式"],response.text)[0]
            self.temp_variables[get_infos["传值变量"]]=value
            # print("获取token的值为:", self.temp_variables[get_infos["传值变量"]], '\n')

        result={'code':'0',
                'response_response':response.reason,
                'response_code':response.status_code,
                'response_header':response.headers,
                'response_body':response.text

                }
        return result

    def __post(self,post_infos):
        url=self.hots+post_infos["请求地址"]

        response = self.seesion.get(url=url,
                                    headers=self.headers,
                                    params=ast.literal_eval(post_infos["请求参数"]),
                                    json=ast.literal_eval(post_infos["请求参数"]))
        response.encoding = response.apparent_encoding


        if post_infos['取值方式'] == "json取值":
            # jsonpath.jsonpath(匹配的字典,'jsonpath取值的表达式')
            value = jsonpath.jsonpath(response.json(), post_infos["取值代码"])[0]
            self.temp_variables[post_infos["传值变量"]] = value
            # print("获取token的值为:", self.temp_variables[post_infos["传值变量"]], '\n')
        elif post_infos["取值方式"] == "正则取值":
            value = re.findall(post_infos["取值代码"], response.text)[0]
            self.temp_variables[post_infos["传值变量"]] = value
            # print("获取token的值为:", self.temp_variables[post_infos["传值变量"]], '\n')

        result = {
            'code':0,  #请求是否成功的标志位
            'response_reason':response.reason,
            'response_code':response.status_code,
            'response_headers':response.headers,
            'response_body':response.text
        }
        return result

    def request(self,step_infos):
        request_type=step_infos['请求方式']
        param_variable_list = re.findall('\\${\w+}', step_infos["请求参数(get)"])
        if param_variable_list:
            for param_values in param_variable_list:
                step_infos["请求参数(get)"] = step_infos["请求参数(get)"].\
                    replace(param_values, '"%s"' % self.temp_variables.get(
                    param_values[2:-1]))
        print("1:", step_infos["请求参数(get)"])
        if request_type=="get":
            result=self.__get(step_infos)

        elif request_type =='post':

            data_variable_list = re.findall('\\${\w+}', step_infos["请求参数(get)"])
            if param_variable_list:
                for param_values in data_variable_list:
                    step_infos["请求参数(get)"] = step_infos["请求参数(get)"].replace(param_values,
                                                                              '"%s"' % self.temp_variables.get(
                                                                                  param_values[2:-1]))
            print("2:", step_infos["请求参数(post)"])

            result=self.__post(step_infos)
        else:
            result={'code':'3',
                    'result':'请求结果不支持'}
        return result

    def request_by_step(self,step_infos):
        self.temp_variables = {}
        for step_info in step_infos:
            temp_result=self.request(step_info)
            if temp_result['code']!=0:
                break
            print(temp_result['response_body'])
        return temp_result

if __name__=="__main__":
    case_info2 = [
        {'请求方式': 'get',
         '请求地址': '/cgi-bin/token',
         '请求参数(get)': '{"grant_type":"client_credential","appid":"wx60536c088aee3040","secret":"f214d833f873d8cc1b38255eca0938d9"}',
         '提交数据（post）': '', '取值方式': 'json取值', '传值变量': 'token', '取值代码': '$.access_token'},
        {'请求方式': 'post', '请求地址': '/cgi-bin/tags/delete', '请求参数(get)': '{"access_token":${token}}',
         '提交数据（post）': '{"tag":{"id":459}}', '取值方式': '无', '传值变量': '', '取值代码': ''}
    ]


    case_info3 = [{'测试用例编号': 'case02',
                 '测试用例名称': '测试能否正确新增用户标签',
                 '用例执行': '否', '测试用例步骤': 'step_01',
                 '接口名称': '获取access_token接口',
                 '请求方式': 'get',
                 '请求地址': '/cgi-bin/token',
                 '请求参数(get)': '{"grant_type":"client_credential","appid":"wx60536c088aee3040","secret":"f214d833f873d8cc1b38255eca0938d9"}',
                 '提交数据（post）': '',
                 '取值方式': 'json取值',
                 '传值变量': 'token',
                 '取值代码': '$.access_token',
                 '期望结果类型': '正则匹配',
                 '期望结果': '{"access_token":"(.+?)","expires_in":(.+?)}'},
                {'测试用例编号': 'case02', '测试用例名称': '测试能否正确新增用户标签',
                 '用例执行': '否',
                 '测试用例步骤': 'step_02',
                 '接口名称': '创建标签接口',
                 '请求方式': 'post',
                 '请求地址': '/cgi-bin/tags/create',
                 '请求参数(get)': '{"access_token":${token}}',
                 '提交数据（post）': '{"tag" : {"name" : "nanyue_8888"}}',
                 '取值方式': '无',
                 '传值变量': '',
                 '取值代码': '',
                 '期望结果类型': '正则匹配',
                 '期望结果': '{"tag":{"id":(.+?),"name":"8888"}}'}]

    get_infos1={'请求方式':'get',
               '请求地址':'cgi-bin/token?',
               '请求参数':"{'grant_type':'client_credential','appid':'wx60536c088aee3040','secret':'f214d833f873d8cc1b38255eca0938d9'}",
               "取值方式": "json取值",
               '取值代码': '$.access_token',
               '传值变量':  None
               }
    get_infos2=[{'请求方式':'get',
               '请求地址':'cgi-bin/token?',
               '请求参数':"{'grant_type':'client_credential','appid':'wx60536c088aee3040','secret':'f214d833f873d8cc1b38255eca0938d9'}",
               "取值方式": "正则取值",
               '取值代码': '"access_token":"(.+?)",',
               '传值变量':  None,
               '请求参数(get)': '{"grant_type":"client_credential","appid":"wx60536c088aee3040","secret":"f214d833f873d8cc1b38255eca0938d9"}',
               }]
    case_info1 = [{'测试用例编号': 'case02', '测试用例名称': '测试能否正确新增用户标签', '用例执行': '否', '测试用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}', '提交数据（post）': '', '取值方式': 'json取值', '传值变量': 'token', '取值代码': '$.access_token', '期望结果类型': '正则匹配', '期望结果': '{"access_token":"(.+?)","expires_in":(.+?)}'},
                  {'测试用例编号': 'case02', '测试用例名称': '测试能否正确新增用户标签', '用例执行': '否', '测试用例步骤': 'step_02', '接口名称': '创建标签接口', '请求方式': 'post', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}', '提交数据（post）': '{"tag" : {"name" : "nanyue_8888"}}', '取值方式': '无', '传值变量': '', '取值代码': '', '期望结果类型': '正则匹配', '期望结果': '{"tag":{"id":(.+?),"name":"8888"}}'}]

    print(   RequestUtils().request_by_step(case_info3))



