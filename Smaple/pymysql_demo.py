import pymysql
import json



class ConnectPymysql():
    def __init__(self):
        self.connect=pymysql.connect(host='172.16.20.145',
                          port=3306,
                          user='xudt',
                          password='Xudt@253',
                          database='test',
                          charset='utf8')

    def data_dict_all(self,sql_str):
        str_data=sql_str
        # 建立游标对象
        current=self.connect.cursor(cursor=pymysql.cursors.DictCursor)
        current.execute(str_data)
        data=current.fetchall()
        return data



if __name__=="__main__":
    str_data='''
        select case_info.case_id as 测试用例编号,case_info.case_name,case_info.is_run,case_step_info.case_step_name,api_info.api_name,api_info.api_request_type,api_info.api_request_url,api_info.api_url_params,api_post_data,case_step_info.get_value_type,case_step_info.variable_name,case_step_info.get_value_code,case_step_info.excepted_result_type,case_step_info.excepted_result
        from case_step_info 
        LEFT JOIN case_info on case_step_info.case_id = case_info.case_id
        LEFT JOIN api_info on case_step_info.api_id = api_info.api_id 
        where case_info.is_run = '是'
        order by case_info.case_id,case_step_info.case_step_name;
        '''
    data=ConnectPymysql().data_dict_all(str_data)
    for case_info in data:
        print(json.dumps(case_info,indent=1,ensure_ascii=False))
