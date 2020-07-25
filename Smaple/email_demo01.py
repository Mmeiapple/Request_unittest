import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# 创建一个邮件信息对象
msg=MIMEText('hello,P1P2','html','utf-8')
msg['from']="505349085@qq.com"
msg['to']='1986812570@qq.com,505349085@qq.com'
msg['Cc']='1986812570@qq.com'
msg['subject']='何梅接口自动化'

# 创建一个服务对象
smtp=smtplib.SMTP()
# 邮件服务器地址
smtp.connect("smtp.qq.com")
# 服务器登录
smtp.login(user="505349085@qq.com",password="dajhtkkzrtrdbhfb")
# 发送信息
smtp.sendmail("505349085@qq.com",["505349085@qq.com","1986812570@qq.com"],msg.as_string())
