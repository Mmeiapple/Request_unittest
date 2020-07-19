import os
from common.request_utils import RequestUtils
from common.testdata_utils import TestdataUtils

current=os.path.dirname(__file__)
data_path=os.path.join(current,'../data/test_case1.xlsx')
print(data_path)

allcase=TestdataUtils('Sheet1').get_testcase_data_list()
for case_info in allcase:

    Result=RequestUtils().request_by_step(case_info.get('case_info'))
    print(Result)
