# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 16:41:54 2021

@author: DALab
"""
import random as ra
from VirtualFactory.Generator import random_date
import datetime
class Customer:
    def __init__(self, name):
        self.name = name
        self.importance = None

    def read_pd_list(self, pd_list):
        self.pd_list = pd_list

    def purchase(self, plan_range):
        purchase_order = {}
        purchase_order['item_name'] = 'pd_'+"%03d" % ra.randint(0, len(self.pd_list)-1)
        purchase_order['item_qty'] = ra.randint(30, 100)
        purchase_order['DD'] = random_date(plan_range[1]-datetime.timedelta(hours=ra.randint(1,3)), plan_range[1])
        return purchase_order
    