"""
# @Time     : 2022/3/1 8:07 上午
# @Author   : ssw
# @File     : helper_mail.py
# @Desc      : 
"""
import smtplib
from email.mime.text import MIMEText
from traceback import format_exc

# 邮件配置信息
mail = None

# 邮件内容缓存
email_context_cache_1 = ''
email_context_cache_2 = ''


def set_mail(_mail):
    """
    设置mail配置参数
    :param const: mail配置参数
    """
    global mail
    # 初始化Redis缓存链接
    try:
        if not mail:
            mail = _mail
    except:
        pass


def send_mail(subject, context, to_list):
    '''
    发送邮件
    接收参数：
    subject 邮件主题
    context 邮件内容
    to_list 接收者邮件列表，每个邮件地址用","分隔
    '''
    if not subject or not context or not to_list:
        return '邮件发送失败，邮件主题、内容与收件人邮件都是必填项'

    # 初始始化邮件相关参数
    email = MIMEText(context, 'html', 'utf-8')
    email_list = list(to_list.split(','))
    email['To'] = ",".join((email_list))
    email['Subject'] = subject
    email['From'] = mail.get('doctor', '')

    # QQ邮箱改为ssl方式发送了
    # s = smtplib.SMTP(smtp)
    s = smtplib.SMTP_SSL(mail.get('smtp', ''))
    try:
        s.login(mail.get('doctor', ''), mail.get('passwd', ''))
        s.sendmail(mail.get('doctor', ''), email_list, email.as_string())
        s.close()
        return None
    except Exception as e:
        s.close()
        stacktrace = format_exc()
        return '邮件发送失败，出现异常：' + str(e.args) + stacktrace + '\n'


def send_error_mail(context):
    '''
    发送邮件
    接收参数：
    context 邮件内容
    '''
    if not context:
        return '邮件内容是必填项'

    # 定义两个变量为全局变量
    global email_context_cache_1, email_context_cache_2
    # 从缓存中读取邮件内容，如果上一封邮件内容与当前内容一样时，则不发送
    if email_context_cache_1 == context or email_context_cache_2 == context:
        return ''
    # 将当前邮件内容存储到服务器缓存中
    email_context_cache_1, email_context_cache_2 = context, email_context_cache_1

    send_mail(mail.get('email_title', ''), context, mail.get('email_list', ''))