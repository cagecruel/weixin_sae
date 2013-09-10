# coding:UTF-8
import hashlib
import web
import lxml
import time
import os
from lxml import etree

import urllib
import xml.etree.ElementTree as ET

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

name = ["名称	   %s\n",
        "时间    %s\n",
        "最新价%s\n",
        "昨收盘  %s\n",
        "今开盘  %s\n",
        "涨跌额  %s\n",
        "最低    %s\n",
        "最高    %s\n",
        "涨跌幅  %s\n",
        "成交量  %s手\n",
        "成交额  %s万"
        ]

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

class WeixinInterface:    
       
    def GET(self):
        # 获取输入参数
        data = web.input()
    	signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        # 自己的token
        token = "southmoneyweixin"
        # 字典序排序
        list = [token, timestamp, nonce]
        list.sort()
        # sha1加密算法
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            # print "true"
            return echostr
       
    def POST(self):
        # 从获取的xml构造xml dom树
        str_xml = web.data()
        xml = etree.fromstring(str_xml)#type str
        # 提取信息
        fromUser = xml.find("FromUserName").text            
        toUser = xml.find("ToUserName").text
        msgType = xml.find("MsgType").text
       
        content = xml.find("Content").text
        # query with the stock number
        url = urllib.urlopen("http://www.webxml.com.cn/WebServices/ChinaStockWebService.asmx/getStockInfoByCode?theStockCode=%s"%content)
        tree = ET.parse(url)
        root = tree.getroot()
               
        # stock name
        content = ""
        #content = name[0]%(root[0].text)
        for i in range(1, len(name) + 1):
            content += name[i-1]%(root[i].text)
       
        # 模板渲染
        return render.reply_text(fromUser, toUser, int(time.time()), msgType, content)