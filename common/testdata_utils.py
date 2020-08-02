import os
import xlrd
import json
from common.excel_utils import Excel_utils


current = os.path.dirname(__file__)
path_data_file = os.path.join(current, '../data/test_case1.xlsx')


class TestdataUtils():
    def __init__(self,sheet_name='Sheet1',test_data_path=path_data_file):
        self.test_data_path=test_data_path
        self.test_data=Excel_utils(path_data_file, sheet_name).get_sheet_data_by_dict()

    def get_testcase_data_dict(self):
        all_case = {}
        for i in self.test_data:
            all_case.setdefault(i['测试用例编号'], []).append(i)
        return all_case
    def get_testcase_data_list(self):
        list_data=[]
        data=self.get_testcase_data_dict()
        for key,value in data.items():
            dict_data={}
            dict_data['case_id']=key
            dict_data['case_info']=value
            list_data.append(dict_data)
        return list_data

    def get_row_number(self,case_id,case_name):
        for row in range(len(self.test_data)):
            if self.test_data[row]['测试用例编号'] == case_id and self.test_data[row]['测试用例步骤'] == case_name:
                break
        return row+1




if __name__=="__main__":
    value =TestdataUtils('Sheet1',path_data_file).get_testcase_data_dict()
    caselist=[]
    for key,value in value.items():
        dictlist = {}
        dictlist['case_name']=key
        dictlist['case_info']=value
        caselist.append(dictlist)
    # value2=TestdataUtils('Sheet1',path_data_file).get_testcase_data_list()
    #
    # print(json.dumps(value2, indent=1, ensure_ascii=False))

    row_number=TestdataUtils('Sheet1',path_data_file).get_row_number('case04','step_02')
    print(row_number)
