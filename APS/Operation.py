# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 21:59:45 2020

@author: RoyTseng
"""
#from APS.Order import Order

class Operation():
    def __init__(self,order_id, op_id, op_t):
        self.order_id = order_id
        self.id = op_id
        self.op_t = op_t

    def __repr__(self):
        return "Op %s"%self.__dict__
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

