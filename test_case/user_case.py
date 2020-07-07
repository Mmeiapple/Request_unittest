import unittest
import re
from com.log_print import Log
from Action.user_management import UserManagement


class WeChat(unittest.TestCase):
    def setUp(self):
        Log.logsinfo('')
        Log.logsinfo('------测试开始了------')

    def test_creat_tag_sucsess(self):
        result=UserManagement().create_label_success()
        tag_name=re.findall('"name":"(.+?)"',result)[0]
        self.assertEqual(result.__contains__(tag_name),True,"创建标签成功执行失败")

    def test_creat_tag_failed_tokenerror(self):
        result=UserManagement().create_tag_failed_tokenerror('423DFSDFFSHDJHKSS')
        error=re.findall('"errcode":(.+?),',result)[0]
        self.assertEqual(result.__contains__(error), True, "token错误，创建标签失败--执行失败")


    def test_create_tag_failed_namelong(self):
        result=UserManagement().create_tag_failed_namelong("标签超出长度限制标签超出长度限制标签超出长度限制标签超出长度限制标签超出长度限制标签超出长度限制")
        error=re.findall('"errcode":(.+?),',result)[0]
        self.assertEqual(result.__contains__(error), True, "标签名过长，创建标签失败--执行失败")

    def test_create_tag_failed_rename(self):
        result=UserManagement().create_tag_failed_rename("湖南")
        error=re.findall('"errcode":(.+?),',result)[0]
        self.assertEqual(result.__contains__(error), True, "标签名重复，创建标签失败--执行失败")

    def test_get_tag_success(self):
        result=UserManagement().get_tag_success()
        tagconetent=re.findall('{"tags":(.+?)}',result)[0]
        self.assertEqual(result.__contains__(tagconetent),True,"获取所有标签成功--执行失败")


    def test_modify_tag_success(self):
        result=UserManagement().modify_tag_success('104','北京')
        content=re.findall('"errmsg":"(.+?)"',result)[0]
        self.assertEqual(result.__contains__(content),True,"成功修改标签--执行失败")


    def tearDown(self):
        Log.logsinfo('')
        Log.logsinfo('------测试结束啦------')

if __name__=="__main__":

    unittest.main(verbosity=2)