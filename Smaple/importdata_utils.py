from common.testdata_utils import TestdataUtils
from common.request_utils import RequestUtils
import json




all_data=TestdataUtils().get_testcase_data_list()
resposne=[]

for case_info in all_data:
    # print(json.dumps(case_info.get('case_info'),ensure_ascii=False,indent=1))
    data_response=RequestUtils().request_by_step(case_info.get('case_info'))
    resposne.append(data_response)
print(resposne)