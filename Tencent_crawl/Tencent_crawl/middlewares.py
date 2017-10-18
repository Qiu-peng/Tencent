# -*- coding: utf-8 -*-

'''
    中间键（参数不用return,会在运行时读取）
'''

# 导入USER_AGENT_LIST
from Tencent_crawl.settings import USER_AGENT_LIST
import random
import base64


# 处理user_agent
class UserAgentMiddlewares(object):
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)

        # request.headers["User-Agent"] = user_agent
        request.headers.setdefault("User-Agent", user_agent)


# 处理代理
class ProxyMiddlewares(object):
    def process_request(self, request, spider):

        # 免费代理的使用,如果是私密代理，就要加上后面的代码
        proxy ="116.62.128.50:16816"
        request.meta["proxy"] = "http://" + proxy

        # 验证代理的账户名和密码
        user_passwd = "mr_mao_hacker:sffqry9r"
        # 将账户名和密码经过base64编码处理
        base64_user_passwd = base64.b64encode(user_passwd)
        # 将处理后的字符串添加到请求报头里,
        request.headers["Proxy-Authorization"] = "Basic " + base64_user_passwd
