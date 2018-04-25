#coding:utf-8
#使用样例
import json
from TradeInterface import RealTimeTrading
trade = RealTimeTrading(userid='18126352115',password='Cloud25683')

trade.set_stock_dic( {'code': '000006', 'volume': '100', 'price': '1', 'price_type': 'now_price', 'effect_term': '2'} )
#进行交易请求

#res = trade.buy() # 买入
#res = trade.sell() # 卖出
temp = json.loads(trade.query_records(startday="2018-4-1", endday="2018-04-26") )# 委托查询
for item in temp:
    if item['revoke'] == 'yes':
        print item['pre_id']
#res = trade.cancel_order(pre_id='20180404111606042') # 撤单
#res = trade.query_history_records(startday="2018-04-04", endday="2018-04-05") # 历史交割查询
#res = trade.query_profit() # 资产查询

#print(res)