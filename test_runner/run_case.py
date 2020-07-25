import os
import unittest
from common.email_utils import EmailUtils
from common import HTMLTestReportCN


crurrent_path=os.path.dirname(__file__)
test_case_path=os.path.join(crurrent_path,'../api_testcase')
test_report_path=os.path.join(crurrent_path,'../test_reports')


class RunCase():
    def __init__(self):
        self.test_case_path=test_case_path
        self.test_report_path=test_report_path
        self.title='api接口自动化测试报告'
        self.description='自动化接口测试为框架'
        self.tester='hemei'
    def load_test_suite(self):
        discover=unittest.defaultTestLoader.discover(start_dir=self.test_case_path,
                                                     pattern='unittest_test.py',
                                                     top_level_dir=self.test_case_path)
        all_testsuite=unittest.TestSuite()
        all_testsuite.addTest(discover)
        return all_testsuite
    def run(self):
        report_dir=HTMLTestReportCN.ReportDirectory(self.test_report_path)
        report_dir.create_dir(self.title)
        report_filepath=HTMLTestReportCN.GlobalMsg.get_value('report_path')
        with open(report_filepath,'wb') as file:
            runner=HTMLTestReportCN.HTMLTestRunner(stream=file,
                                                   title=self.title,
                                                   description=self.description,
                                                   tester=self.tester)
            runner.run(self.load_test_suite())
        return report_filepath



if __name__=="__main__":
    report_path=RunCase().run()
    print(report_path.split('\\')[-1])
    EmailUtils('接口自动化测试报告',report_path).send_mail()