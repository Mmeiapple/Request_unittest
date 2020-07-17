import re
import ast


class CheckUtils():
    def __init__(self, response_data):
        self.ck_response = response_data

        self.check_rules = {
            '无':self.no_check,
            'json键是否存在': self.check_key,
            'json键值对': self.check_key_value,
            '正则匹配': self.check_regexp
                           }
        self.pass_result = {
            'code': 0,
            'response_reason': self.ck_response.reason,
            'response_code': self.ck_response.status_code,
            'response_headers': self.ck_response.headers,
            'response_body': self.ck_response.text,
            'check_result': True,
            'message': ''  # 扩招作为日志输出等
        }
        self.fail_result = {
            'code': 2,
            'response_reason': self.ck_response.reason,
            'response_code': self.ck_response.status_code,
            'response_headers': self.ck_response.headers,
            'response_body': self.ck_response.text,
            'check_result': False,
            'message': ''  # 扩招作为日志输出等
        }

    '''
    检查json键是否存在
    
    '''

    def check_key(self, check_data=None):
        check_data_list = check_data.split(',')

        expdata = self.ck_response.json()

        # 存放每次比较的结果
        res_list = []
        # 存放比较失败key
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

    '''检查键值对'''

    def check_key_value(self,check_data=None):
        expdata = self.ck_response.json()

        # 存放每次比较的结果
        res_list = []
        # 存放比较失败key
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
    
    '''
    def check_regexp(self,check_data=None):

        if re.findall(check_data,self.ck_response):
            return self.pass_result
        else:
            return self.fail_result


    '''
    
    无断言
    
    '''

    def no_check(self):
        return self.pass_result

    '''
    
    驱动调用断言
    
    '''
    def run_check(self,check_rules,check_data):
        if self.ck_response.status_code == 200:
            if check_rules in self.check_rules.keys():
                    result=self.check_rules[check_rules](check_data)
                    return result
            else:
                self.fail_result['message']='%s不支持该方式的断言'%check_data
                return self.fail_result
        else:
            self.fail_result['message'] = '响应状态码为%s' % self.ck_response.status_code
            return self.fail_result


if __name__=="__main__":
    str1='{"access_token":"(.+?)","expires_in":(.+?)}'
    response1='{"access_token":"34Wsaklllsdassa","expires_in":7200}'
    str2 = 'access_token,expires_in'
    response2='{"access_token":"34Wsaklllsdassa","expires_in":7200}'
    str3='{"expires_in":7200}'
    response3='{"access_token":"34Wsaklllsdassa","expires_in":7200}'
    print(CheckUtils(response1).check_regexp(str1))
