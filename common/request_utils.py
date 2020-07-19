import os
import ast
import requests
import jsonpath
import re
import json
import random
from common.check_utils import CheckUtils
from common.get_config import getconfig
from common.testdata_utils import TestdataUtils
from requests.exceptions import RequestException
from requests.exceptions import ProxyError
from requests.exceptions import ConnectionError



class RequestUtils():
    def __init__(self):
        self.hots = getconfig.geturl
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
        try:
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

            result = CheckUtils(response).run_check(get_infos['期望结果类型'],get_infos['期望结果'])
        except ProxyError as e:
            result={'code':4,'result':'请求【%s】失败，代理错误异常'%get_infos['接口名称']}
        except ConnectionError as e:
            result={'code':4,'result':'请求【%s】失败，连接超时异常'%get_infos['接口名称']}
        except RequestException as e:
            result={'code':4,'result':'请求【%s】失败，Request异常，原因：%s'%(get_infos['接口名称'],e.__str__())}
        except Exception as e:
            result={'code':4,'result':'请求【%s】失败，系统异常，原因：%s'%(get_infos['接口名称'],e.__str__())}
        return result

    '''调用post请求'''

    def __post(self, post_info):
        try:
            url = self.hots + post_info["请求地址"]
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

            result = CheckUtils(response).run_check(post_info['期望结果类型'],post_info['期望结果'])
        except ProxyError as e:
            result={'code':4,'result':'请求【%s】失败，代理错误异常'%post_info['接口名称']}
        except ConnectionError as e:
            result={'code':4,'result':'请求【%s】失败，连接超时异常'%post_info['接口名称']}
        except RequestException as e:
            result={'code':4,'result':'请求【%s】失败，Request异常，原因：%s'%(post_info['接口名称'],e.__str__())}
        except Exception as e:
            result={'code':4,'result':'请求【%s】失败，系统异常，原因：%s'%(post_info['接口名称'],e.__str__())}
        return result

    '''请求判断'''

    def request(self, step_info):
        try:
            request_type = step_info["请求方式"]
            param_variable_list = re.findall('\\${\w+}', step_info["请求参数(get)"])
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
        except Exception as e:
            result = {'code': 4, 'result': '测试用例：%s的 %s步骤出现了系统异常，原因:%s'%
                      (step_info['测试用例编号'],step_info["测试用例步骤"],e.__str__())}
        return result

    '''多个测试用例分别执行'''
    def request_by_step(self, step_infos):
        self.temp_variables = {}
        for step_info in step_infos:
            temp_result = self.request(step_info)
            if temp_result['code'] != 0:
                break
        return temp_result


if __name__ == "__main__":
    current = os.path.dirname(__file__)
    path_data_file = os.path.join(current, '../data/test_case1.xlsx')
    value2 = TestdataUtils('Sheet1', path_data_file).get_testcase_data_list()
    case01=value2[0]['case_info']
    case02=value2[1]['case_info']
    case03=value2[2]['case_info']
    case04=value2[3]['case_info']
    # print(json.dumps(case03,indent=1,ensure_ascii=False))

    a=RequestUtils().request_by_step( case04 )
    print(a)
