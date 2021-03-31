# -*- coding:utf-8 -*-
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.header import Header
# 发件人地址，通过控制台创建的发件人地址
username = ''#写阿里邮箱
# 发件人密码，通过控制台创建的发件人密码
password = ''#阿里邮箱的密码
# 自定义的回复地址
replyto = '***'
# 收件人地址或是地址列表，支持多个收件人，最多30个
#rcptto = ['17863118591@163.com']
rcptto = '17863118591@163.com'


def listTostr(notice):
    #根据传入的参数不同来构建返回字符串
    temp=""
    if(type(notice)==type([])):
        for item in notice:
            temp+='{}\n'.format(item)
        return temp
    if(type(notice)==type("")):
        return notice


def sendmail(notice,recever):
    notice=listTostr(notice)
    # 构建alternative结构
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header('打工仔最新状态提醒')
    msg['From'] = '%s <%s>' % (Header('KunAli mailbox'), username)
    msg['To'] = recever
    msg['Reply-to'] = replyto
    msg['Message-id'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate() 
    # 构建alternative的text/plain部分
    # textplain = MIMEText('测试内容', _subtype='plain', _charset='UTF-8')
    # msg.attach(textplain)
    textplain = MIMEText(notice, _subtype='plain', _charset='UTF-8')
    msg.attach(textplain)
    # 构建alternative的text/html部分
    # texthtml = MIMEText('网页部分', _subtype='html', _charset='UTF-8')
    # msg.attach(texthtml)
    # 发送邮件
    try:
        # client = smtplib.SMTP()
        #python 2.7以上版本，若需要使用SSL，可以这样创建client
        client = smtplib.SMTP_SSL()
        #SMTP普通端口为25或80
        client.connect('smtp.aliyun.com',465)
        #开启DEBUG模式
        client.set_debuglevel(0)
        client.login(username, password)
        #发件人和认证地址必须一致
        #备注：若想取到DATA命令返回值,可参考smtplib的sendmaili封装方法:
        #      使用SMTP.mail/SMTP.rcpt/SMTP.data方法
        client.sendmail(username, recever, msg.as_string())
        client.quit()
        print('邮件发送成功！')
    except smtplib.SMTPConnectError as e:
        print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as e:
        print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPDataError as e:
        print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        print('邮件发送失败, ', str(e))
    except Exception as e:
        print('邮件发送异常, ', str(e))

    
if __name__=='__main__':
    notice=""
    lists=['王城了','失败']
    # for item in lists:
    #     notice+='{}工作异常\n'.format(item)
    # sendmail(notice)
    listTostr(lists)