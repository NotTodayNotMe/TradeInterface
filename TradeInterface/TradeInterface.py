# encoding: utf-8
"""
@author: cb_Lian
@version: 1.0
@license: Apache Licence
@file: TradeInterface.py
@time: 2018/3/13 16:11
@Function：This interface is designed for people who use haizhi licai to realise
           simulate-trading stocks
"""
import json
import urllib2
import urllib
import hashlib

class Trade:
    """
    参数说明：1.userId，用户Id，需在海知平台注册获得，默认'',必须设置
              2.password，用户密码，海知平台注册时用户所设，默认'',必须设置
              3.buy_sell，买卖操作,'buy' 或 'sell' , 默认'',必须设置
              4.buy_price，设置买入某只股票的价格，默认'' ，若不设置，将会按照市价(买一)进行操作
              5.sell_price，设置卖掉某只股票的价格，默认'' ，若不设置，将会按照市价(卖一)进行操作
              6.volume，设置买卖股票的数量，默认‘average_all’,若不设置，默认买入时可用剩余资金在每只股票平均分配，
                        卖出时全部卖出，若设置数量，则按所能实际买卖的数量与设置的数量取最小值交易
              7.code，买卖股票的代码，默认'',必须设置

    """

    def __init__(self, userid='', password=''):
        self.send_dic = {'userid': userid.strip(), 'password': self.md5encryption(password), 'stock_dic_ls': list()}
        self.url = 'http://192.168.0.136/Tradeinterface/get_tradeinfo'

    # set userid of user of haizhi licai
    def set_userid(self, userid):
        if userid.strip() != '':
            self.send_dic['userid'] = userid
            return True
        else:
            return False

    # set password of haizhi licai
    def set_password(self, password):
        if password.strip() != '':
            self.send_dic['password'] = self.md5encryption(password)
            return True
        else:
            return False

    # set stocks_ls of your own stocks,the type is list,and each elemnet of it is dictionary
    def set_stock_dic_ls(self, stock_dic_ls):
        if len(stock_dic_ls) > 0:
            self.send_dic['stock_dic_ls'] = stock_dic_ls
            return True
        else:
            return False

    # return the template of stock_dic
    def get_stock_dic(self):
        stock_dic = {'buy_sell': '', 'buy_price': '', 'sell_price': '', 'volume': 'average_all', 'code': ''}
        return stock_dic

    # 实现md5加密
    def md5encryption(self, password):
        if password.strip() != '':
            md = hashlib.md5()
            md.update(password.encode(encoding='utf-8'))
            return md.hexdigest()
        else:
            return ''

    # post the request to haizhi licai,and return the result
    def http_post(self):
        # 用户id为空
        if self.send_dic['userid'] == '':
            return "userid attribute can't be a blank string"
        # 用户密码为空
        if self.send_dic['password'] == '':
            return "password attribute can't be a blank string"
        temp_stock_dic_ls = self.send_dic['stock_dic_ls']
        # 用户的股票信息为空
        if len(temp_stock_dic_ls) == 0:
            return "stock info must be needed"
        else:
            for stock_dic in temp_stock_dic_ls:
                # 用户的买卖标志为空
                if stock_dic['buy_sell'] == '':
                    return "buy_sell attribute can't be a blank string"
                # 用户的股票代码为空
                if stock_dic['code'] == '':
                    return "code attribute can't be a blank string"
        # 数据暂时没有问题，json编码提交
        jdata = json.dumps(self.send_dic)  # 对数据进行json格式化编码
        # print jdata
        jdata = urllib.urlencode({'tradeinfo': jdata})  # urlencode编码
        req = urllib2.Request(self.url, jdata)  # 生成页面请求的完整数据
        res = urllib2.urlopen(req)  # 发送页面请求
        return res.read()  # 返回结果

