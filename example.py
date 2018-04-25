#coding:utf-8
#使用样例

from TradeInterface import RealTimeTrading
trade = RealTimeTrading(userid='18126352115',password='Cloud25683')

trade.set_stock_dic( {'code': '000006', 'volume': '100', 'price': '1', 'price_type': 'now_price', 'effect_term': '2'} )
#进行交易请求

res = trade.buy() # 买入
#res = trade.sell() # 卖出
#res = trade.query_records(startday="2018-4-4", endday="2018-04-05") # 委托查询
#res = trade.cancel_order(pre_id="201804040948554657") # 撤单
#res = trade.query_history_records(startday="2018-04-04", endday="2018-04-05") # 历史交割查询
#res = trade.query_profit() # 资产查询

print(res)