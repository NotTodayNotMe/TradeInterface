#coding:utf-8

import datetime
import json
from HistoryTrading import HistoryTrading
from RealTimeTrading import RealTimeTrading

'''装饰器'''
def input_checker(func):
    '''
    用于监测函数输入是否合法，code,volume均转化为str
    :param func:
    :return:
    '''
    def _input_checker(self,**kwargs):
        # 股票代码检查
        if isinstance(kwargs['code'], str):
            pass
        elif isinstance(kwargs['code'], int):
            kwargs['code'] = str(kwargs['code'])
            while len(kwargs['code']) < 6:
                kwargs['code'] = '0' + kwargs['code']
        else:
            raise TypeError, 'code must be str or int'
        # 股票交易量检查
        if isinstance(kwargs['volume'], str):
            pass
        elif isinstance(kwargs['volume'], int):
            kwargs['volume'] = str(kwargs['volume'])
        else:
            raise TypeError, 'volume must be str or int'
        #回测日期检查
        if isinstance(self._core,HistoryTrading):
            if 'date' not in kwargs:
                kwargs['date'] = self._current_time.strftime('%Y-%m-%d')
            elif isinstance(kwargs['date'],datetime.datetime):
                kwargs['date'] = datetime.datetime.strftime('%Y-%m-%d')
            elif isinstance(kwargs['date'],str):
                pass
            else:
                raise TypeError,'date must be str or datetime object'
        #返回函数
        print kwargs
        res = func(self, **kwargs)
        return res
    return _input_checker


class TestEngine(object):

    def __init__(self,user_id='',password = '',type = 'RealTimeTrading'):
        '''
        {'buy_sell': 'sell', 'code': '000006', 'volume': '100', 'price': '1', 'price_type': 'now_price', 'effect_term': '2'}
        :param user_id:用户id
        :param password: 用户密码
        :param type: 交易引擎类型，默认为实盘交易引擎
        :param stratagy_name: 交易策略名称，默认为空，当选用回测引擎时，必填
        '''
        if type == 'RealTimeTrading':
            self._core = RealTimeTrading(userid=user_id, password=password)
        elif type == 'HistoryTrading':
            stratagy_name = user_id
            self._current_time = datetime.datetime.today()-datetime.timedelta(days=1)
            self._core = HistoryTrading(userid=user_id,password=password,strategy_name = stratagy_name)
            self._core.create_strategy(stratagy_name)
        else:
            raise ValueError,'type must be "RealTimeTrading" or "HistoryTrading"'
    #显示当前的交易引擎类型
    @property
    def core(self):
        return self._core.__class__
    #显示当前回测引擎时间
    @property
    def current_time(self):
        if isinstance(self._core,RealTimeTrading):
            return datetime.datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
        elif isinstance(self._core,HistoryTrading):
            return self._current_time.strftime('%Y-%m-%d')

    @current_time.setter
    def current_time(self,date):
        if isinstance(self._core,HistoryTrading):
            if isinstance(date,str):
                self._current_time = datetime.datetime.strptime(date,'%Y-%m-%d')
            elif isinstance(date,datetime.datetime):
                pass
        else:
            raise TypeError, '%s can not operate on current_time' % (self._core.__class__)

    def shift_current_time(self,days):
        if isinstance(self._core,RealTimeTrading):
            raise TypeError,'RealTimeTrading can not operate on current_time'
        elif isinstance(self._core,HistoryTrading):
            self._current_time += datetime.timedelta(days=days)
            return self._current_time.strftime('%Y-%m-%d')
    #购买
    @input_checker
    def buy(self,code,volume,price_type='now_price',price=None,date=None):
        if isinstance(self._core,RealTimeTrading):
            dic = {'code':code,
                   'volume':volume,
                   'price_type': price_type,
                   'price': price,
                   'effect_term':'2'}
            self._core.set_stock_dic(dic)
            res = self._core.buy()
            return json.loads(res)
        elif isinstance(self._core,HistoryTrading):
            dic = {'date':date,
                   'code': code,
                   'volume': volume,
                   'price_type': 'average_price',
                   }
            self._core.set_stock_dic(dic)
            res = self._core.bt_buy()
            return json.loads(res)
    #卖出
    @input_checker
    def sell(self,code,volume,price_type='now_price',price=None,date=None):
        if isinstance(self._core,RealTimeTrading):
            dic = {'code':code,
                   'volume':volume,
                   'price_type': price_type,
                   'price': price,
                   'effect_term':'2'}
            self._core.set_stock_dic(dic)
            res = self._core.sell()
            return json.loads(res)
        elif isinstance(self._core,HistoryTrading):
            dic = {'date': date,
                   'code': code,
                   'volume': volume,
                   'price_type': 'average_price',
                   }
            self._core.set_stock_dic(dic)
            res = self._core.bt_sell()
            return json.loads(res)
    #撤单
    def cancel_order(self):
        pass
    #资产和持仓情况
    def query_profit(self):
        if isinstance(self._core, RealTimeTrading):
            return json.loads(self._core.query_profit())
        elif isinstance(self._core,HistoryTrading):
            pass

    #历史交割查询
    def query_history_records(self,start='',end=''):
        if isinstance(self._core,RealTimeTrading):
            return json.loads(self._core.query_history_records(start,end))
        elif isinstance(self._core,HistoryTrading):
            return json.loads(self._core.bt_query_history_records(start, end))
    #历史交割单输出到csv文件
    def history_to_csv(self,path='history_record'):
        if isinstance(self._core,RealTimeTrading):
            pass
        elif isinstance(self._core,HistoryTrading):
            return self._core.get_history_csv(path)
    #查询策略
    def list_stratagy(self):
        if isinstance(self._core,HistoryTrading):
            return json.loads(self._core.get_strategy())
        else:
            raise AttributeError, '%s has no attribute stratagy_name' % (self._core.__class__)
    # 设置策略名称
    def set_stratagy(self, stratagy_name):
        if isinstance(self._core, HistoryTrading):
            self._core.set_strategy_name(stratagy_name)
        else:
            raise AttributeError, '%s has no attribute stratagy_name' % (self._core.__class__)
    #删除策略
    def del_stratagy(self,stratagy_name):
        if isinstance(self._core,HistoryTrading):
            return self._core.del_strategy(stratagy_name)
        else:
            raise AttributeError, '%s has no attribute stratagy_name' % (self._core.__class__)





