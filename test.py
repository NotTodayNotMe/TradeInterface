#coding:utf-8
from TradeInterface import TestEngine
import datetime
import json

'''实盘交易引擎示例'''
user_id ='18126352115'
password = 'Cloud25683'
def Realtime():
    '''
    实盘交易引擎
    :return:
    '''
    Engine = TestEngine(user_id=user_id,password=password,type='RealTimeTrading')
    print Engine.core
    print Engine.current_time
    #print Engine.buy(code='600848',volume=100)
    #print Engine.sell(code='600848', volume=100)
    temp = Engine.query_records(start="2018-04-25", end="2018-04-26")
    print len(temp)
    print temp[0]['pre_id']
    print Engine.cancel_order(str(temp[0]['pre_id']))
    print Engine.query_history_records(start="2018-4-4", end="2018-04-05")
    print Engine.query_profit()
'''历史回测引擎示例'''
def History():
    '''
    历史回测引擎
    :return:
    '''
    Engine = TestEngine(user_id=user_id,password=password,type='HistoryTrading')
    print Engine.core
    print Engine.current_time
    print Engine.list_stratagy()
    if Engine.list_stratagy():
        Engine.del_stratagy(Engine.list_stratagy()[0]['strategy_name'])
        Engine.create_stratagy(user_id)
        Engine.set_stratagy(user_id)
    else:
        Engine.create_stratagy(user_id)
        Engine.set_stratagy(user_id)
    print Engine.buy(code =600848,volume=1000,date = '2017-10-11')
    Engine.current_time = '2018-4-8'
    Engine.shift_current_time(1)
    print Engine.current_time
    print Engine.sell(code='600848',volume=100)
    print Engine.history_to_csv('data')


if __name__ == '__main__':
    #Realtime()
    History()
'''
Engine.shift_current_time(-20)
print Engine.core
#print Engine.del_stratagy(Engine.list_stratagy()[0]['strategy_name'])
print Engine.list_stratagy()[0]

print Engine.list_stratagy()
print Engine.buy(code =600848,volume=1000)
temp = json.loads(Engine.query_history_records())

for dic in temp[1:]:
    for item in dic:
        print item,dic[item]
Engine.shift_current_time(2)
print Engine.sell(code =600848,volume=100)

#print Engine.current_time
#print type(Engine.current_time)
#print Engine.shift_current_time(1)
'''


