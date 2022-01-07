# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 16:32:48 2021

@author: DALab
"""
import pandas as pd 
from Product import gen_pd_list
from Process import gen_pc_list
from Customer import Customer
import random as ra
import datetime
import sys
import os,sys

class Factory:
    def __init__(self):
        self.path = os.getcwd()
        self.pc_list = gen_pc_list(10, (3,5), (2,3), (0,2), (0,2))
        self.pd_list = gen_pd_list(10, (3,6))
        self.pd_pc_map = self.gen_pd_pc_map(self.pd_list, self.pc_list, 4)
        self.orders = {}
    #規劃產品與相對應的製程資訊
    def gen_pd_pc_map(self, pd_list, pc_list, least_Npc:4):
        pd_pc_map = {}
        for pd in pd_list:
            pd_pc_map[pd.id] = []
            rnd_pc_list_idx = ra.sample(range(len(pc_list)), ra.randint(least_Npc, len(pc_list)))
            rnd_pc_list_idx = sorted(rnd_pc_list_idx)
            for i in range(len(rnd_pc_list_idx)):
                pd_pc_map[pd.id].append(pc_list[i])
        return pd_pc_map
    #拿產品資訊給顧客看, 顧客下單
    def meet_customers(self, purchase_horizon, cust_list, CURRENTTIME):
        for cust in cust_list:
            cust.read_pd_list(self.pd_list)
            order = cust.purchase(purchase_horizon)
            order['wo_create_time'] = CURRENTTIME-datetime.timedelta(hours = ra.randint(2,15))
            self.orders[cust.name] = order
    #回傳規劃時間之內的工單 
    def get_target_orders(self, target_time):
        order_list = []
        for key, order in self.orders.items():
            if order['DD']<target_time:            
                order_list.append(order)
        return order_list
    
    #產生虛擬工單資料
    def gen_order_data(self):
        row_list = []
        #隨機開始與結束時間
        # start = datetime.datetime.strptime('2008/1/1 1:30 PM', '%Y/%m/%d %I:%M %p')
        # end = datetime.datetime.strptime('2008/2/1 1:30 PM', '%Y/%m/%d %I:%M %p')
        counter = 0
        for key, item in self.orders.items():
            date = item['DD']-datetime.timedelta(hours=ra.randint(2,15))
            dict1 = {'data_fetch_time': item['wo_create_time'],
                      'data_create_time': item['wo_create_time'],
                      'order_id':'wo_'+"%03d" % counter,
                      'pd_id':item['item_name'],
                      'qty':item['item_qty'],
                      # 'route_id':'route_'+"%03s" % item['item_name'][-3:],
                      'ES': date,
                      'DD': item['DD']
                    }
            counter+=1
            row_list.append(dict1)
        self.data = pd.DataFrame(row_list)
        self.data.to_excel(self.path+'/fake_order_data.xlsx', sheet_name='order', index=False)  

    #幫每一個product建立route路徑
    def gen_route_table(self):
        def gen_pd_route(pd, pd_pc_map):
            pc_list = pd_pc_map[pd.id]
            row_list = []
            final = False
            for idx, pc in enumerate(pc_list):
                if idx == (len(pc_list)-1):
                    final_op = True
                final_op = 'op_'+"%01d" % (idx+1)+"0"
                if final:
                    final_op = ''
                mcg_id = ra.choice(pc.mcg_list).id
                dict1 = {'pd_id': pd.id,
                         'op_id':'op_'+"%01d" % idx+"0",
                         'su_t':ra.randint(20, 30),
                         'op_t':ra.randint(50, 120),
                         'next_op':final_op,
                         'mc_group_id': mcg_id,
                         'is_crr':ra.randint(0,1),
                         'is_claw':ra.randint(0,1),
                         'is_ft':ra.randint(0,1)
                        }
                row_list.append(dict1)
            return row_list
        row_list = []
        for product in self.pd_list:
            route_list = gen_pd_route(product, self.pd_pc_map)
            row_list.extend(route_list)
        data = pd.DataFrame(row_list)
        data.to_excel(self.path+'/fake_route_table.xlsx', sheet_name='order',index=False)
        
    #中繼資料表1 機群與機台對照表
    def gen_mcg_mc_table(self):
        row_list = []
        for pc in self.pc_list:
            for mcg in pc.mcg_list:
                for mc in mcg.mc_list:
                    dict1 = {'mcg_id':mcg.id,
                             'mc_id':mc.id
                            }
                    row_list.append(dict1)
        data = pd.DataFrame(row_list)
        data.to_excel(self.path+'/mcg_mc_table.xlsx', sheet_name='order',index=False)
        
    #中繼資料表2 機台與治具對照表
    def gen_mc_ft_table(self):
        row_list = []
        for pc in self.pc_list:
            for mcg in pc.mcg_list:
                for mc in mcg.mc_list:
                    for ft in mc.ft_list:
                        dict1 = {'mc_id':mc.id,
                                 'ft_id':ft.id
                                }
                        row_list.append(dict1)
        data = pd.DataFrame(row_list)
        data.to_excel(self.path+'/mc_ft_table.xlsx', sheet_name='order',index=False)
        
    # def gen_pd_restrict_table(self):
    #     for pd in pd_list:
            
    
    
    # def gen_rs_table(self):
    #     pc_list = self.pd_list
    #     row_list= []
        
    #     for pd_id, pc_list in self.pd_pc_map:             
    #         for pc in pc_list:
    #             dict1 = {'rs_id':pd_id + pc.id,
    #                      'Mc_group_id': pc.mc_list[ra.randint(0, len(pc.mc_list))].id,
    #                      'Nft':ra.randint(2, 3)
    #                      }
    #         row_list.append(dict1)
    #     self.data = pd.DataFrame(pc_list)
    #     self.data.to_excel(self.path+'/fake_process_data.xlsx', sheet_name='order', index=False)
        
# ##創建虛擬工廠
# fac = Factory()
# #接客數, 產生虛擬客戶
# Ncust = 35
# cust_list = [Customer('cust_%03d'% i) for i in range(Ncust)]
# CURRENTTIME = pd.to_datetime('20200902090006')
# start = datetime.datetime.strptime('2008/1/1 1:30 PM', '%Y/%m/%d %I:%M %p')
# end = datetime.datetime.strptime('2008/4/1 1:30 PM', '%Y/%m/%d %I:%M %p')
# #設定客戶下單範圍
# purchase_horizon = (start, end)
# #將客戶給工廠，工廠將產品資訊交給客戶，客戶挑選產品，並制定交期
# fac.meet_customers(purchase_horizon, cust_list, CURRENTTIME)
# fac.gen_order_data()
# fac.gen_route_table()
# fac.gen_mcg_mc_table()
# fac.gen_mc_ft_table()



