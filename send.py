import zmail

# 发送提醒的邮箱
SENDER = 'sender mail addr'

# 126邮箱开通stmp后这里填写授权码
PASSWD = 'your password'

# 接收提醒的邮箱
RECEIVER = 'receiver mail addr'

SERVER = zmail.server(SENDER, PASSWD)
