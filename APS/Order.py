# -*- coding: utf-8 -*-
"""
Title: Job Shop Scheduling Module
Version: 0.1
Author: Kuan-Chen Tseng k.c.tseng@ie.nthu.edu.tw
Copyright: Belongs to DAlab Solutions x Associates Co.,Ltd.
"""

import datetime
import copy
class Order:
    def __init__(self, order_id, pd_id, ES, DD):
        #General
        self.id = order_id
        self.pd_id = pd_id
        self.ES = ES
        self.DD = DD
        self.init_ES = ES
        self.cur_op_idx = 0
        self.op_list = []
    def add_attr(self, attr, value):
        setattr(self, attr, value)
        
    #當這張工單的當前工序完成後，通知下一個工序的可開始時間。#待測試
    def reset(self):
        self.ES = self.init_ES
        self.cur_op_idx = 0
        
    def target_next_op(self):
        self.cur_op_idx+=1
        
    def get_target_op(self):
        return self.op_list[self.cur_op_idx]

    def __repr__(self):
        return "%s"%self.__dict__
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    