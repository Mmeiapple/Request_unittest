import os
import warnings
import unittest
import paramunittest
from common.testdata_utils import TestdataUtils
from common.request_utils import RequestUtils

current = os.path.dirname(__file__)
path_data_file = os.path.join(current, '../data/test_case1.xlsx')
case_info=TestdataUtils('Sheet1', path_data_file).get_testcase_data_list()
@paramunittest.parametrized(
    *case_info
)

class UtestParamunittest(paramunittest.ParametrizedTestCase):

    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)

    def setParameters(self, case_id, case_info):
        self.case_id=case_id
        self.case_info=case_info

    def test_api_function(self):
        '''

        测试描述

        '''
        self._testMethodName = self.case_info[0].get("测试用例编号")
        self._testMethodDoc = self.case_info[0].get("测试用例名称")
        actual_result=RequestUtils().request_by_step(self.case_info)
        print(actual_result.get('check_result'))
        self.assertTrue(actual_result.get('check_result'),actual_result.get('message'))

if __name__=='__main__':
    unittest.main()