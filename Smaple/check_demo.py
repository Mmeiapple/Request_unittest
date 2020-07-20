import re
import ast
from typing import Dict, Any, Union


class CheckUtils():
    def __init__(self, response_data):
        self.ck_response = response_data

        self.check_rules = {
            '无': self.no_check,
            'json键是否存在': self.check_key,
            'json键值对': self.check_key_value,
            '正则匹配': self.check_regexp
        }
        # self.pass_result = {
        #     'code': 0,
        #     'response_reason': self.ck_response.reason,
        #     'response_code': self.ck_response.status_code,
        #     'response_headers': self.ck_response.headers,
        #     'response_body': self.ck_response.text,
        #     'check_result': True,
        #     'message': ''  # 扩招作为日志输出等
        # }
        # self.fail_result = {
        #     'code': 2,
        #     'response_reason': self.ck_response.reason,
        #     'response_code': self.ck_response.status_code,
        #     'response_headers': self.ck_response.headers,
        #     'response_body': self.ck_response.text,
        #     'check_result': False,
        #     'message': ''  # 扩招作为日志输出等
        # }

    '''
    
    检查json键或则key来进行断言
    
        res_list:存放每次比较的结果
        wrong_key:存放比较失败key    
        先对预期结果进行分割，写入列表 
        循环比遍历实际结果的键值对与预期结果的键对进行比较，成功就在res_list加Ture，失败加False
        如果res_list中有False，代表断言失败
        例：    
            预期结果 = 'access_token,expires_in'
            实际结果 = '{"access_token":"123fadfsad","expires_in":7200}'
            断言结果 =  True 

    '''

    def check_key(self, check_data=None):
        check_data_list = check_data.split(',')

        expdata = self.ck_response.json()

        res_list = []

        wrong_key = []

        for value in check_data_list:
            if value in expdata.keys():
                res_list.append(True)
            else:
                res_list.append(False)
                wrong_key.append(value)
                print(wrong_key)
        if False in res_list:
            return self.fail_result
        else:
            return self.pass_result

    '''
    检查键值对
        res_list:存放每次比较的结果
        wrong_key:存放比较失败key     
        循环比遍历实际结果的键值对与预期结果的键值对进行比较，成功就res_list加Ture
        如果res_list中有False，代表断言失败
        例：    
            预期结果 = '{"expires_in":7200}'
            实际结果 = '{"access_token":"123fadfsad","expires_in":7200}'
            断言结果 =  True      
          
    '''

    def check_key_value(self, check_data=None):
        expdata = self.ck_response
        res_list = []
        wrong_key = []
        for value in ast.literal_eval(check_data).items():
            if value in expdata.items():
                res_list.append(True)
            else:
                res_list.append(False)
                wrong_key.append(value)
        if False in res_list:
            return self.fail_result
        else:
            return self.pass_result

    '''
    正则检查
    
     # 判断能否从实际接果中匹配到预期结果的值，有就返回成功结果，没有就返回失败的结果
     
     例：    预期结果 = '{"access_token":"(.+?)","expires_in":(.+?)}'
            实际结果 = '{"access_token":"123fadfsad","expires_in":7200}'
            断言结果 =  True

    '''

    def check_regexp(self, check_data=None):


        if re.findall(check_data, self.ck_response):

            return True
        else:
            return False

    '''

    无断言

    '''

    def no_check(self):
        return self.pass_result

    '''

    驱动调用断言
    
    先判断返回的code码是不是等于200
    循环遍历出断言方式是否存在断言规则中
    如果存在则调用该方法
    self.check_rules[check_rules](check_data)  等于 self.check_key(check_data)

    '''

    def run_check(self, check_rules, check_data):
        if self.ck_response.status_code == 200:
            if check_rules in self.check_rules.keys():
                result = self.check_rules[check_rules](check_data)
                return result
            else:
                return False
        else:
            return False


if __name__ == "__main__":
    str1 = '{"access_token":"(.+?)","expires_in":(.+?)}'
    response1 = '{"access_token":"123fadfsad","expires_in":7200}'
    str2 = 'access_token,expires_in'
    response2 = '{"access_token":"34Wsaklllsdassa","expires_in":7200}'
    str3 = '{"expires_in":7200}'
    response3 = '{"access_token":"34Wsaklllsdassa","expires_in":7200}'
    print(CheckUtils(response1).check_regexp(str1))

