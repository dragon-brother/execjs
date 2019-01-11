#coding:utf-8

import requests
import urllib
import re
from urlparse import urljoin
import json
import time
# from readability.readability import Document
from lxml import html
import execjs


url = 'https://bbs.rednet.cn/forum.php?mod=guide&view=newthread'



s = requests.Session()
headers1 = {
"Host":"bbs.rednet.cn",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
"Accept-Encoding":"gzip, deflate, br",
"Connection":"keep-alive",
"Upgrade-Insecure-Requests":"1",
}
r = s.get(url,headers=headers1)
# r.encoding = r.apparent_encoding
js_content = r.text
# print '0000000000000000000',r.text
print s.cookies.get_dict()
__jsluid = s.cookies.get_dict().get('__jsluid')
js_cont = re.findall(r'(var x.*)\<\/script\>',js_content)#第一次返回源码
if js_cont:
    js_cont = js_cont[0]
    # print '11111111111111111111111',js_cont
    eval_str = re.findall(r'eval(\(.*?\))\;',js_cont,re.S|re.I)[0]#匹配出eval的字符串
    eval_str = eval_str.replace('z','z+1')#while(z++)之后执行z+1
    # print '@@@@@@@@@@@@@@@@@@@@',eval_str
    eval_str = 'function jsstr(){return%s};'%eval_str#创建函数返回eval字符串
    # print '2222222222222222',eval_str
    var_str = js_cont.split('while(z++)')[0]#js定义参数
    # print '333333333333333333',var_str
    js_cont1 = var_str + eval_str#拼接后的js
    # print '#################',js_cont1
    ctx = execjs.compile(js_cont1)
    js_cont2 = ctx.call('jsstr')
    print '22222222222222222',js_cont2#要eval的字符串
    cookie_str = js_cont2.split('.cookie')[-1].split('};if')[0]
    cookie_str = 'cookie' + cookie_str
    cookie_str = re.sub(r'document.*?firstChild\.href', r'"https://bbs.rednet.cn/"', cookie_str)#定义document这类环境里没有的参数
    cookie_str = re.sub(r'window\[.*?\]','undefined',cookie_str)#替换window['callP' + 'hantom']此类
    cookie_str = cookie_str.replace('window.headless','undefined')
    print '3333333333333333333',cookie_str
    cookies_update = ctx.eval(cookie_str)
    __jsl_clearance = re.findall('(__jsl_clearance=.*?);',cookies_update)[0]
    cook = '__jsluid={};{}'.format(__jsluid,__jsl_clearance)
    print '44444444444444444', cook
    # cook_list = cookies_update.split(';')
    # cook_dict = {}
    # for each in cook_list:
    #     if each:
    #         each = each.split('=')
    #         key = each[0]
    #         value = each[1]
    #         cook_dict[key] = value


    headers = {
        "Host": "bbs.rednet.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://bbs.rednet.cn/forum.php?mod=guide&view=newthread",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cookie": '__jsluid={};{}'.format(__jsluid,__jsl_clearance),
    }
    # cook_dict = {"Cookie": '__jsluid={};{}'.format(__jsluid,cookies_update)}
    # # cookies = requests.utils.cookiejar_from_dict(cook_dict, cookiejar=None, overwrite=True)
    s.headers.update(headers)#直接整个headers更新进去
    # print 'ssssssssssssss',s.headers
    r2 = s.get(url)
    print 'cccccccccccc', r2.cookies.get_dict(),r2.status_code
    print r2.text
