# -*- coding: utf-8 -*-
"""
Title: Job Shop Scheduling Module
Version: 0.1
Author: Kuan-Chen Tseng k.c.tseng@ie.nthu.edu.tw
Copyright: Belongs to DAlab Solutions x Associates Co.,Ltd.
"""
# import pandas as pd

from Data.DataTrans import create_orders_operations, create_rs_dict
from VirtualFactory.Machine import Machine, MachineGroup
import pandas as pd
import os

class Data:
    def __init__(self, fac, CURRENTTIME):
        self.fac = fac
        self.path = os.getcwd()+'/Data/fake_data'
        self.CURRENTTIME = CURRENTTIME
        self.__read_fake_data()
        self.__load_factory_data()
        
    def __read_fake_data(self):
        path = self.path
        self.order_data = pd.read_excel(path+'/fake_order_data.xlsx', sheet_name='order')
        self.route_table = pd.read_excel(path+'/fake_route_table.xlsx', sheet_name='order')
        
        #創建Order物件List
        self.mc_ft_table = pd.read_excel(path+'/mc_ft_table.xlsx', sheet_name='order')
        self.mcg_mc_table = pd.read_excel(path+'/mcg_mc_table.xlsx', sheet_name='order')
        
        #預處理填空值
        self.route_table['ft_id'].fillna('', inplace=True)
        #傳入工單資訊、途程檔、治具檔, 工廠製程資訊
        self.orders, self.all_op_list = create_orders_operations(self.order_data, self.route_table, self.CURRENTTIME)
        self.mcg_dict, self.ft_dict = create_rs_dict(self.fac.pc_list)
        self.wip_bucket_dict = self.fac.wip_bucket
        
    def __load_factory_data(self):
        self.mcg_dict = self.fac.mcg_dict
        
    #每次解碼前必須reset
    def reset(self):
        #reset order
        for key, order in self.orders.items():
            order.reset()
        #reset resource
        for key, mcg in self.mcg_dict.items():
            mcg.reset()
            for mc in mcg.mc_list:
                bucket = self.wip_bucket_dict[mc.id]
                mc.reset(bucket)
        
# data = Data()
