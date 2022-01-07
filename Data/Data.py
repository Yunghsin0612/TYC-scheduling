# -*- coding: utf-8 -*-
"""
Created on Thu May  7 15:35:30 2020

@author: DALab
"""
# import pandas as pd

# from DataTrans import create_orders_operations, create_rs_dict
# from VirtualFactory.Machine import Machine, MachineGroup
import sys
import os
sys.path.append('../APS')
import pandas as pd
import os
import copy
import pickle
import datetime
from Data.DataTrans import create_orders, create_all_op_list, create_mcg_dict
from Data.Others import load_machines
# , decode_forbidden
class Data:
    def __init__(self, CURRENTTIME):
        self.path = os.getcwd()+'\Data\TYC_data'
        self.CURRENTTIME = datetime.datetime.strptime('2021/2/26 12:00 AM', '%Y/%m/%d %I:%M %p')
        self.__read_data()
        # self.__data_cleaning()
        self.__data_transform()
        self.__data_load()
        
    def __read_data(self):
        self.df = pd.read_excel(self.path+'/tyc_wo.xlsx', sheet_name = None)      
        self.wo_table = self.df["wo"]
        # self.wo_table = self.df["wo"]
        # self.wip_table= self.df["WIP"]
        # self.route_bom = self.df["route_bom"]
        self.mcg_table = self.df["機群情境與人機比"]
        # self.materail_storage = self.df["物料表與成品庫存"]
        # self.staff = self.df["人員班表"]
        # self.PPAD = self.df["pm計畫與非計畫停機"]
        # self.mc_status = self.df["機台狀態"]
        # self.mc_fitness = self.df["機台配適度"]
        
    def __data_cleaning(self):
        self.wip = wip_cleaning(self.wip_table)
        self.route_bom = route_bom_cleaning(self.route_bom)
        
    def __data_transform(self):
        #產生工單
        self.orders_dict = create_orders(self.wo_table, self.CURRENTTIME)
        self.op_dict, self.mcg_dict, self.mc_dict = create_mcg_dict(self.mcg_table)
        # print(self.orders_dict)
        #將工序資訊納入工單
        # set_op_list_to_order(self.orders_dict, self.route_bom)
        # #TODO 生成機群假資料 (之後資料完備可以拔掉這行)
        # self.mcg_table = extend_mcg_table(self.mcg_table, self.route_bom)
        # #生成工作站-層別字典，用來索引機群
        # self.op_layer_mcg_dict, self.mcg_dict, self.mc_dict = create_process_data(self.mcg_table)
        
        # #TODO 之後由過往排程結果的order之DD獲得(目前隨機產生)
        # self.wip_opder_DD = get_DD_for_wip(self.wip)
        # self.wip_orders = create_wip_orders(self.wip, self.route_bom, self.CURRENTTIME, self.wip_opder_DD)
        self.all_op_list = create_all_op_list(self.orders_dict)
        # self.forbidden_info = create_forbidden_info(self.PPAD, self.CURRENTTIME)
        
        #分成新的虛擬wip工單 和 凍結其之內的wip 
        #TODO先讀機群表再說
        # classify_wip(self.wip_table, self.CURRENTTIME)
        # create_wip_bucket(self.wip, self.route_bom, self.CURRENTTIME)
        
    def __data_load(self):
        #讀取所有Machine
        self.schedule = load_machines(self.mc_dict)
        #禁線時間先排
        # self.forbidden_schedule = decode_forbidden(self.forbidden_info, schedule, self.mc_dict)
        # #再排wip
        # self.wip_schedule = decode_wip(self, self.forbidden_schedule)
        # #save forbidden and wip information 
        self.wip_pickle = pickle.dumps(self.schedule)
    
    #每次解碼完將資料回歸至解碼前的狀態
    def reset(self):
        # reset order
        for key, order in self.orders_dict.items():
            order.reset()
        # reset resource

        for key, mcg in self.mcg_dict.items():
            for mc in mcg[0].mc_list:
                mc.reset()

        return pickle.loads(self.wip_pickle)

# data = Data()
# print(data.all_op_list)
