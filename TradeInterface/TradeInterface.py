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
import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


class Trade:
    """
    参数说明：1.userId，用户Id，需在海知平台注册获得，默认'',必须设置
              2.password，用户密码，海知平台注册时用户所设，默认'',必须设置
              3.cash_ratio 预留现金的比例，0到1之间
              4.buy_sell，买卖操作,'buy' 或 'sell' , 默认'',必须设置
              5.buy_price，设置买入某只股票的价格，默认'' ，若不设置，将会按照市价(买一)进行操作
              6.sell_price，设置卖掉某只股票的价格，默认'' ，若不设置，将会按照市价(卖一)进行操作
              7.volume，设置买卖股票的数量，默认‘average_all’,若不设置，默认买入时可用剩余资金在可购买股票中平均分配，
                        卖出时全部卖出，若设置数量，则按所能实际买卖的数量与设置的数量取最小值交易
              8.code，买卖股票的代码，默认'',必须设置

    """

    def __init__(self, userid='', password='', cash_ratio=''):
        self.send_dic = {'userid': '', 'password': '', 'cash_ratio':'', 'stock_dic_ls': list()}
        self.set_userid(userid)
        self.set_password(password)
        self.set_cash_ratio(cash_ratio)
        self.url = 'http://www.haizhilicai.com/Tradeinterface/get_tradeinfo'

    def set_cash_ratio(self, cash_ratio):
        cash_ratio = str(cash_ratio)
        if self.isnumber(cash_ratio) is True:
            self.send_dic['cash_ratio'] = cash_ratio
            return True
        else:
            return False

    # set userid of user of haizhi licai
    def set_userid(self, userid=''):
        userid = str(userid)
        if userid.strip() != '':
            self.send_dic['userid'] = userid
            return True
        else:
            return False

    # set password of haizhi licai
    def set_password(self, password=''):
        password = str(password)
        if password.strip() != '':
            self.send_dic['password'] = self.md5encryption(password)
            return True
        else:
            return False

    # set stocks_ls of your own stocks,the type is list,and each elemnet of it is dictionary
    def set_stock_dic_ls(self, stock_dic_ls=list()):
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
            md.update(password)
            return md.hexdigest()
        else:
            return ''

    # 判断字符串是否是浮点数
    def isnumber(self, astring):
        try:
            float(astring)
            return True
        except:
            return False

    # 验证现金比例是否是大于0小于1的浮点数
    def validate_cash_ratio(self, cash_ratio):
        if self.isnumber(cash_ratio) is True:
            if float(cash_ratio) < 0.0 or float(cash_ratio) > 1.0:
                return "cash_ratio should be between 0 and 1 !"
            else:
                return True
        else:
            return "cash_ratio should be float!"

    # post the request to haizhi licai,and return the result
    def http_post(self):
        # 用户id为空
        if self.send_dic['userid'] == '':
            return "userid attribute can't be a blank string!"
        # 用户密码为空
        if self.send_dic['password'] == '':
            return "password attribute can't be a blank string!"
        # 验证现金比例是否大于0小于1的浮点数
        if self.validate_cash_ratio(self.send_dic['cash_ratio'])is not True:
            return self.validate_cash_ratio(self.send_dic['cash_ratio'])
        temp_stock_dic_ls = self.send_dic['stock_dic_ls']
        # 用户的股票信息为空
        if len(temp_stock_dic_ls) == 0:
            return "stock info must be needed!"
        else:  # 检验每条股票单的键和值否正确
            for stock_dic in temp_stock_dic_ls:
                tempset = set(['buy_sell', 'code', 'volume', 'buy_price', 'sell_price'])
                tempset = set(stock_dic.keys()) - tempset
                if (len(stock_dic) == 5) and (len(tempset) == 0):
                    # 用户的买卖标志不是buy 或sell
                    if not stock_dic['buy_sell'] in ['buy', 'sell']:
                        return "buy_sell attribute must be buy or sell!"
                    # 用户的股票代码不是数字，尚未判断是否有效:是否是六位，是否存在此代码
                    if not str(stock_dic['code']).isdigit():
                        return "code attribute must be positive number!"
                    # 股数如果不为average_all，检查是否是100 的倍数
                    if stock_dic['volume'] != 'average_all':
                        if not str(stock_dic['volume']).isdigit():  # 设置的字符串不是正整数
                            return "volume must be positive int!"
                        elif (int(str(stock_dic['volume'])) % 100) != 0:  # 判断是否是100 的倍数
                            return "volume must be multiple of 100!"
                    # buy_price是否是''or 浮点数
                    if stock_dic['buy_price'] != '':
                        if self.isnumber(str(stock_dic['buy_price'])) is False:
                            return "buy_price must be positive float!"
                    # sell_price是否是'' or 浮点数
                    if stock_dic['sell_price'] != '':
                        if self.isnumber(str(stock_dic['sell_price'])) is False:
                            return "sell_price must be positive float!"
                else:
                    return "stock_dic must be five normal elements!"
        # 数据暂时没有问题，json编码提交
        jdata = json.dumps(self.send_dic)  # 对数据进行json格式化编码
        # print jdata
        jdata = urllib.urlencode({'tradeinfo': jdata})  # urlencode编码
        req = urllib2.Request(self.url, jdata)  # 生成页面请求的完整数据
        res = urllib2.urlopen(req)  # 发送页面请求
        temp_res = res.read()  # 返回结果，把list结果处理为字符串显示
        try:
            resls = json.loads(temp_res)
            res_str = ""
            for x in resls:
                res_str = res_str + x + '\n'
        except:
            res_str = temp_res
        return res_str

if __name__  == '__main__':
    trade = Trade()
    print trade.isnumber(10)