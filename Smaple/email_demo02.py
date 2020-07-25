import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 发送附件

# 创建一个邮件信息对象
msg=MIMEMultipart()
msg.attach(MIMEText('hello,附件发送','html','utf-8'))
msg['from'] = "505349085@qq.com"
msg['to'] = '1986812570@qq.com,505349085@qq.com'
msg['Cc'] = '1986812570@qq.com'
msg['subject'] = '何梅接口自动化'


# 创建附件对象

attach_file = MIMEText(open('test.txt','rb').read(),'base64','utf-8')
attach_file['Content-Type'] = 'application/octet-stream'
attach_file.add_header('Content-Disposition', 'attachment', filename=('GBK','','test.txt'))
msg.attach( attach_file )

# 创建一个服务对象
smtp=smtplib.SMTP()
# 邮件服务器地址
smtp.connect("smtp.qq.com")
# 服务器登录
smtp.login(user="505349085@qq.com",password="dajhtkkzrtrdbhfb")
# 发送信息
smtp.sendmail("505349085@qq.com",["505349085@qq.com","1986812570@qq.com"],msg.as_string())
