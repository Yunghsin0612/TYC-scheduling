# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 22:04:28 2021

@author: RoyTseng
"""
import random as ra
# from Generator import random_date
# from Process import gen_pc_list
import datetime

class Product:
    def __init__(self, Npc, pd_id):
        #需要的製程數
        self.id = pd_id
        self.Npc = Npc
    def __repr__(self):
        return "Product %s" % self.id
    def __str__(self):
        return "Product %s " % self.id
    
#產生產品資訊
def gen_pd_list(Npd, Rpc:(3, 6)):
    pd_list = []
    for i in range(Npd):
        pd = Product(ra.randint(Rpc[0], Rpc[1]), 'pd_'+"%03d"%i)
        pd_list.append(pd)
    return pd_list



#客戶下單


# start = datetime.datetime.strptime('2008/1/1 1:30 PM', '%Y/%m/%d %I:%M %p')
# end = datetime.datetime.strptime('2008/4/1 1:30 PM', '%Y/%m/%d %I:%M %p')
# purchase_horizon = (start, end)
# requests = customer_purchase(purchase_horizon, 35)
#取得planning horizon的訂單。
def get_request(requests, CURRENTTIME, target_time):
    request_list = []
    for key, request in requests.items():
        if request['DD']<target_time:            
            request_list.append(request)
    return request_list

# target_time = datetime.datetime.strptime('2008/2/1 1:30 PM', '%Y/%m/%d %I:%M %p')
# request_list = get_request(requests, start, target_time)


