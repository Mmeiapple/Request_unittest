import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from common.get_config import getconfig

class EmailUtils():
    def __init__(self,smtp_body,smtp_attch_path=None):
        self.smtp_server=getconfig.get_smtp_server
        self.smtp_sender=getconfig.get_smtp_sender
        self.smtp_password=getconfig.get_smtp_password
        self.smtp_receiver=getconfig.get_smtp_receiver
        self.smtp_cc=getconfig.get_smtp_cc
        self.smtp_subject=getconfig.get_smtp_subject
        self.smtp_body=smtp_body
        self.smtp_attch_path=smtp_attch_path

    def mail_message_body(self):
        message=MIMEMultipart()
        message['from']=self.smtp_sender
        message['to']=self.smtp_receiver
        message['Cc']=self.smtp_cc
        message['subject']=self.smtp_subject
        message.attach(MIMEText(self.smtp_body,'html','utf-8'))
        if self.smtp_attch_path:
            attach_file=MIMEText(open(self.smtp_attch_path,'rb').read(),'base64','utf-8')
            attach_file['Content-Type'] = 'application/octet-stream'
            attach_file.add_header('Content-Disposition', 'attachment', filename=('GBK', '', self.smtp_attch_path.split('\\')[-1]))
            message.attach(attach_file)
        return message
    def send_mail(self):
        smtp=smtplib.SMTP()
        smtp.connect( self.smtp_server )
        smtp.login(user=self.smtp_sender,password=self.smtp_password)
        # lista=[]
        # lista=self.smtp_receiver.
        smtp.sendmail(self.smtp_sender,
                      self.smtp_receiver.split(",")+self.smtp_cc.split(","),
                      self.mail_message_body().as_string())

if __name__=="__main__":
    smtp_attch_path=os.path.dirname(__file__)+'/../Smaple/test.txt'
    EmailUtils('测试报告',smtp_attch_path).send_mail()