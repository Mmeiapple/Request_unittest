import requests
import random
import json
from common.get_token import GetToken
from common.get_config import getconfig


number=random.randint(1,1000)

class UserManagement():
    def __init__(self):
        self.url=getconfig.geturl
        self.token=GetToken(getconfig.getappid,getconfig.getsecret).get_token()
        self.headcontent={'Content-Type': 'application/json'}
        self.creat_url='cgi-bin/tags/create?'
        self.get_tag='cgi-bin/tags/get?'
        self.modify_tag='cgi-bin/tags/update?'


    """
    
    成功创建用户标签
    
    """

    def create_label_success(self):
        headersinfo =  self.headcontent
        data={'access_token':self.token}
        tagname='标签'+str(number)
        jsoninfo={   "tag" : {     "name" : tagname } }
        response=requests.post(url=self.url+self.creat_url,
                               params=data,headers=headersinfo,data=json.dumps(jsoninfo)
                               )
        return response.content.decode('utf-8')

    """

    token错误，创建标签失败

    """

    def create_tag_failed_tokenerror(self,errortoken):
        headersinfo =  self.headcontent
        data = {'access_token': errortoken}
        tagname = '标签' + str(number)
        jsoninfo={   "tag" : {     "name" : tagname } }
        response=requests.post(url=self.url+self.creat_url,
                               params=data,headers=headersinfo,
                               data=json.dumps(jsoninfo))
        return response.content.decode('utf-8')

    """

    标签名过长，创建标签失败

    """

    def create_tag_failed_namelong(self,longtag):
        headersinfo= self.headcontent
        data={'access_token':self.token}
        tagname=longtag+str(number)
        jsoninfo={   "tag" : {     "name" : tagname } }
        response=requests.post(url=self.url+self.creat_url,
                               params=data,
                               headers=headersinfo,
                               data=json.dumps(jsoninfo))
        return response.content.decode('utf-8')

    """

    标签名重复，创建标签失败

    """

    def create_tag_failed_rename(self,tag):
        headersinfo= self.headcontent
        data={'access_token':self.token}
        jsoinfo={  "tag" : {     "name" : tag } }
        response=requests.post(url=self.url+self.creat_url,
                               params=data,
                               headers=headersinfo,
                               data=json.dumps(jsoinfo))
        return response.content.decode('utf-8')

    """

    成功获取公众号已创建的标签

    """
    def get_tag_success(self):
        data={'access_token':self.token}
        response=requests.get(self.url+self.get_tag,params=data)
        return response.content.decode('utf-8')


    """
    成功修改标签内容
    
    """

    def modify_tag_success(self,id,name):
        headersinfo = self.headcontent
        data={'access_token':self.token}
        jsoninfo={   "tag" : {     "id" : id,     "name" : name   } }
        response=requests.post(url=self.url+self.modify_tag,
                               data=json.dumps(jsoninfo),
                               params=data,
                               headers=headersinfo)
        return response.content.decode('utf-8')

if __name__=="__main__":

 tagname=UserManagement().get_tag_success()
 print(tagname);

