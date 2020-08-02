import pymysql

class SqlUtils():
    def __init__(self):
        self.connect = pymysql.connect(
                                    host='172.16.20.145',
                                    port=3306,
                                    user='xudt',
                                    password='Xudt@253',
                                    database='test',
                                    charset='utf8' )
        self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
    def get_mysql_case_info(self):
        str_sql='''
        select case_info.case_id as 测试用例编号,case_info.case_name as 测试用例名称,
        case_info.is_run as 用例执行,case_step_info.case_step_name as 测试用例步骤,
        api_info.api_name as 接口名称,api_info.api_request_type as 请求方式,
        api_info.api_request_url as 请求地址,api_info.api_url_params as 请求参数（get）,
        api_post_data as 提交数据（post）,case_step_info.get_value_type as 取值方式,
        case_step_info.variable_name as 传值变量,case_step_info.get_value_code as 取值代码,
        case_step_info.excepted_result_type as 期望结果类型
        ,case_step_info.excepted_result as 期望结果
        from case_step_info 
        LEFT JOIN case_info on case_step_info.case_id = case_info.case_id
        LEFT JOIN api_info on case_step_info.api_id = api_info.api_id 
        where case_info.is_run = '是'
        order by case_info.case_id,case_step_info.case_step_name;
        '''
        self.cursor.execute(str_sql)
        data_list=self.cursor.fetchall()
        return data_list


if __name__=="__main__":

    sqlutils=SqlUtils().get_mysql_case_info()
    for case_info in sqlutils:
        print(case_info)