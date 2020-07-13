import requests
import re
from common.get_config import getconfig
class GetToken:
    def __init__(self,appid,secret):
        data={'grant_type':'client_credential','appid':appid,'secret':secret}
        self.response=requests.get(url=getconfig.geturl+'cgi-bin/token?',params=data)
        self.body=self.response.content.decode('utf-8')

    def get_token(self):
        token=re.findall('"access_token":"(.+?)"',self.body)[0]
        return token
if __name__=="__main__":
    token=GetToken(getconfig.getappid,getconfig.getsecret).get_token()
    print(token)