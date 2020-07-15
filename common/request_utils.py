import os
import ast
import requests
import jsonpath
import re
import json
import random
from common.get_config import getconfig


class RequestUtils():
    def __init__(self):
        self.hots = 'https://api.weixin.qq.com'
        self.headers = {"ContentType": "application/json;charset=utf-8"}
        self.session = requests.session()
        self.temp_variables = {}

    '''
    
    【调用get请求】
    
    ast.literal_eval:将参数转化为字典
    
    jsonpath.jsonpath(匹配的字典,'jsonpath取值的表达式'),对值进行替换
    
    code:0  请求成功的标志位
    
    '''

    def __get(self, get_infos):
        url = self.hots + get_infos["请求地址"]
        response = self.session.get(url=url,
                                    params=ast.literal_eval(get_infos["请求参数(get)"]))
        response.encoding = response.apparent_encoding
        if get_infos["取值方式"] == "json取值":
            value = jsonpath.jsonpath(response.json(), get_infos["取值代码"])[0]
            self.temp_variables[get_infos["传值变量"]] = value
        elif get_infos["取值方式"] == "正则取值":
            value = re.findall(get_infos["取值方式"], response.text)[0]
            self.temp_variables[get_infos["传值变量"]] = value
        result = {
            'code': 0,
            'response_reason': response.reason,
            'response_code': response.status_code,
            'response_headers': response.headers,
            'response_body': response.text
        }
        return result

    '''调用post请求'''

    def __post(self, post_info):
        url = self.hots + post_info["请求地址"]
        # data = post_infos["提交数据（post）"],
        response = self.session.post(
            url=url,
            headers=self.headers,
            params=ast.literal_eval(post_info["请求参数(get)"]),
            json=ast.literal_eval(post_info["提交数据（post）"])
        )
        response.encoding = response.apparent_encoding
        if post_info["取值方式"] == "json取值":
            value = jsonpath.jsonpath(response.json(), post_info["取值代码"])[0]
            self.temp_variables[post_info["传值变量"]] = value
        elif post_info["取值方式"] == "正则取值":
            value = re.findall(post_info["取值代码"], response.text)[0]
            self.temp_variables[post_info["传值变量"]] = value
        result = {
            'code': 0,  # 请求是否成功的标志位
            'response_reason': response.reason,
            'response_code': response.status_code,
            'response_headers': response.headers,
            'response_body': response.text
        }
        return result

    '''请求判断'''

    def request(self, step_info):
        request_type = step_info["请求方式"]
        param_variable_list = re.findall('\\${\w+}', step_info["请求参数(get)"])
        print("param_variable_list=", param_variable_list)
        if param_variable_list:
            for param_variable in param_variable_list:
                step_info["请求参数(get)"] = step_info["请求参数(get)"].\
                    replace(param_variable, '"%s"' % self.temp_variables.get(param_variable[2:-1]))
        if request_type == "get":
            result = self.__get(step_info)
        elif request_type == "post":
            data_variable_list = re.findall('\\${\w+}', step_info["提交数据（post）"])
            if data_variable_list:
                for param_variable in data_variable_list:
                    step_info["提交数据（post）"] = step_info["提交数据（post）"] \
                        .replace(param_variable, '"%s"' % self.temp_variables.get(param_variable[2:-1]))
            result = self.__post(step_info)
        else:
            result = {'code': 1, 'result': '请求方式不支持'}
        return result

    '''多个测试用例分别执行'''
    def request_by_step(self, step_infos):
        self.temp_variables = {}
        for step_info in step_infos:
            temp_result = self.request(step_info)
            if temp_result['code'] != 0:
                break
            print("测试用例一 【%s】,【返回结果】：%s" % (str(step_info['测试用例名称']), temp_result['response_body']))
        return temp_result


if __name__ == "__main__":
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

    get_infos1 = [
        {'测试用例编号': 'case01',
         '测试用例名称': '测试能否正确执行获取access_token接口',
         '用例执行': '是',
         '测试用例步骤': 'step_01',
         '接口名称': '获取access_token接口',
         '请求方式': 'get',
         '请求地址': '/cgi-bin/token',
         '请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}',
         '提交数据（post）': '',
         '取值方式': '无',
         '传值变量': '',
         '取值代码': '',
         '期望结果类型': 'json键是否存在',
         '期望结果': 'access_token,expires_in'}]
    get_infos2 = [{'请求方式': 'get',
                   '请求地址': 'cgi-bin/token?',
                   '请求参数(get)': "{'grant_type':'client_credential','appid':'wx60536c088aee3040','secret':'f214d833f873d8cc1b38255eca0938d9'}",
                   '提交数据（post）': '',
                   "取值方式": "正则取值",
                   '取值代码': '"access_token":"(.+?)",',
                   '传值变量': None,
                   }]
    case_info1 = [
        {'测试用例编号': 'case02', '测试用例名称': '测试能否正确新增用户标签', '用例执行': '否', '测试用例步骤': 'step_01', '接口名称': '获取access_token接口',
         '请求方式': 'get', '请求地址': '/cgi-bin/token',
         '请求参数(get)': '{"grant_type":"client_credential","appid":"wx60536c088aee3040","secret":"f214d833f873d8cc1b38255eca0938d9"}',
         '提交数据（post）': '', '取值方式': 'json取值', '传值变量': 'token', '取值代码': '$.access_token', '期望结果类型': '正则匹配',
         '期望结果': '{"access_token":"(.+?)","expires_in":(.+?)}'},
        {'测试用例编号': 'case02', '测试用例名称': '测试能否正确新增用户标签', '用例执行': '否', '测试用例步骤': 'step_02', '接口名称': '创建标签接口',
         '请求方式': 'post', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}',
         '提交数据（post）': '{"tag" : {"name" : "nany1_8888"}}', '取值方式': '无', '传值变量': '', '取值代码': '', '期望结果类型': '正则匹配',
         '期望结果': '{"tag":{"id":(.+?),"name":"8888"}}'}]

    a=RequestUtils().request_by_step( case_info1 )
    # a={'code': 0, 'response_reason': 'OK', 'response_code': 200, 'response_headers': {'Connection': 'keep-alive', 'Content-Type': 'application/json; encoding=utf-8', 'Date': 'Tue, 14 Jul 2020 09:49:39 GMT', 'Content-Length': '194'}, 'response_body': '{"access_token":"35_kbbJmtj5twTVL5r3kh8YlkOhq85s_3NluPAsTUwmJqftq8FSHXhqoBLN0Ckm_NHuMd8LD-zj2yOIccuX_NH53kgwqYWvZg0fr8G-Yx-dXjk3bvjzH6eYHSJEETwp49bPCEUuc8fIr0MXPTDPSUAhADAYAG","expires_in":7200}'}
    print(a)
    # a = get_infos1[0]['请求参数(get)']
    # params = ast.literal_eval(get_infos1[0]["请求参数(get)"])
    # print("无转化:%s" % a)
    # print("转化后:%s" % params)
    # print(type(a))
