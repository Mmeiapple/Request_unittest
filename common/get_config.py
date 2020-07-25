import os
from configparser import ConfigParser


current=os.path.dirname(__file__)
filepath=os.path.join(current,'../config/conf.ini')

class GetConfig():
    def __init__(self):
        self.__conf=ConfigParser()
        self.__conf.read(filepath,encoding='utf-8')

    #自定义传值获取配置信息
    def getindependent(self,configuration,name):
        return self.__conf.get(configuration,name)
    """
    
    默认测试地址
    
    """
    @property  #将方法变为属性
    def geturl(self):
        return self.__conf.get('defaule','url')

    """

    appid

    """

    @property  # 将方法变为属性
    def getappid(self):
        return self.__conf.get('defaule', 'appid')

    """

    secret

    """

    @property  # 将方法变为属性
    def getsecret(self):
        return self.__conf.get('defaule', 'secret')



    '''
    
    【邮件发送测试报告信息】
    邮箱服务器 smtp_server
    邮箱账号 smtp_sender
    授权码 smtp_password
    收件人 smtp_receiver
    抄送人 smtp_cc
    邮件主题 smtp_subject
    
    
    '''
    @property
    def get_smtp_server(self):
        return self.__conf.get('email', 'smtp_server')

    @property
    def get_smtp_sender(self):
        return self.__conf.get('email', 'smtp_sender')

    @property
    def get_smtp_password(self):
        return self.__conf.get('email', 'smtp_password')

    @property
    def get_smtp_receiver(self):
        return self.__conf.get('email', 'smtp_receiver')

    @property
    def get_smtp_cc(self):
        return self.__conf.get('email', 'smtp_cc')

    @property
    def get_smtp_subject(self):
        return self.__conf.get('email', 'smtp_subject')




getconfig=GetConfig()


if __name__=="__main__":
    print(getconfig.get_smtp_server)
    print(getconfig.get_smtp_subject)

