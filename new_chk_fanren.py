"""
使用xpath跟踪特定网页内容更简单
version 0.21    2018-10-21
version 0.2     2018-10-20
"""

import requests
from lxml import etree
from send import SENDER, PASSWD, RECEIVER, SERVER
import time
import logging

loggingfile = 'logfile'
logging.basicConfig(
                    level=logging.DEBUG, format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s', datefmt='%Y-%m-%d %A %H:%M:%S',                                     # 时间
                    filename = loggingfile,
                    filemode = 'a') 

url = 'https://book.qidian.com/info/1010734492'

sleep_time = 600


def getNewChapter():
    """取得最新章节数及章节名
    """
    try:
        r = requests.get(url, timeout=10)
    except requests.exceptions.Timeout as err: #发生异常以后暂停60秒，重新调用自己
        logging.critical(err)
        time.sleep(30)
        try:
            getNewChapter()   
        except RecursionError as err:   #防止服务器长时间无法访问递归调用到最大数，log一下
            logging.critical(err)    
    html = etree.HTML(r.text)
    # xpath路径
    path = html.xpath('/html/body/div[2]/div[6]/div[4]/div[1]/div[1]/div[2]/ul/li[2]/div/p[1]/a')
    r.encoding='utf-8'
    for string in path:
        return string.text

# 实例化最新章节内容
lastChapter = getNewChapter()
logging.info(lastChapter + ' 为最新章节')
mail_content = {
            'subject': getNewChapter() + ' 已更新',
            'content': '快去看一看', }

while True:
    time.sleep(sleep_time)

    if lastChapter != getNewChapter():
        mail_content = {
                        'subject': getNewChapter() + ' 已更新',
                        'content': '快去看一看', }
        lastChapter = getNewChapter()
        logging.info('已更新' + lastChapter)
        SERVER.send_mail(RECEIVER, mail_content)        
    else:
        logging.info('没有更新')
