# -*- coding: utf-8 -*-
"""
Title: Job Shop Scheduling Module
Version: 0.1
Author: Kuan-Chen Tseng k.c.tseng@ie.nthu.edu.tw
Copyright: Belongs to DAlab Solutions x Associates Co.,Ltd.
"""

import datetime
import pandas as pd
import random as ra
import numpy as np
from collections import defaultdict
import math
from dateutil import tz

# from APS.Bucket import Bucket
# from APS.Block import Block
from APS.Order import Order
from APS.Operation import Operation
from APS.Operation import Operation
from Factory.Machine import Machine, MachineGroup
#秒
#TODO透過Route查詢工時的行為模式，取德時間
# =============================================================================
# 1.ORDER
# =============================================================================
def create_operations(order_id, virtual_pd_id, route_bom):
    specific_row = route_bom[(route_bom['pd_id'] == virtual_pd_id)]
    op_list = []
    for idx, row in specific_row.iterrows():
        idx = row['idx']
        op_id = row['op_id']
        op_t = row['op_t']
        op = Operation(idx, op_id, op_t)
        # TODO 之後可以用dictionary將額外欄位用append_special生成物件
        pd_id = row['pd_id']
        layer = row['layer']
        
        setattr(op, 'pd_id', pd_id)
        setattr(op, 'layer', layer)
        setattr(op, 'order_id', order_id)
        op_list.append(op)
    return op_list

def create_all_op_list(orders_dict):
    all_op_list = []
    for key, order in orders_dict.items():
        all_op_list.extend(order.op_list)
    return all_op_list

def set_op_list_to_order(orders_dict, route_bom):
    for key, order in orders_dict.items():
        order_id = order.id
        virtual_pd_id = order.virtual_pd_id
        op_list = create_operations(order_id, virtual_pd_id, route_bom)
        setattr(order, 'op_list', op_list)
        
def create_orders(wo_route_table, CURRENTTIME):
    CURRENTTIME_timestamp = CURRENTTIME.timestamp()
    def retrieve(row):
        wo_data = {}
        #General , Never Change!
        order_id = row['工單號碼']
        pd_id = row['品號'] 
        #ES = datetime.datetime.strptime(str(row['可加工時間']), '%Y-%m-%d %H:%M:%S')
        #TODO之後分開預處理與轉換物件  
        #判斷交貨日期欄位若為缺值給定交貨日期無限大
        if pd.isna(row['交貨日期']):
            DD = 99999
            ES = 9999
        else:
            DD = datetime.datetime.strptime(str(int(row['交貨日期'])), '%Y%m%d')
            #TYC尚未給定可加工時間，先預設隨機交貨日期減5到30天
            # ES = DD - datetime.timedelta(days=ra.randint(5,30))
            ES = 0
            DD = DD.timestamp()
            # ES = ES.timestamp()
        #最早可加工時間>0
        ES = max(ES - CURRENTTIME_timestamp, 0)
        DD = DD - CURRENTTIME_timestamp
        
        
        order = Order(order_id, pd_id, ES, DD)   
        #TODO Special, Change along with problems
        
        #TYC工單資訊新增屬性
        setattr(order, 'quantity', row['開單數'])
        setattr(order, 'material1', row['原料1'])
        setattr(order, 'material2', row['原料2'])
        setattr(order, 'material3', row['原料3'])
        setattr(order, 'ft_id', row['治具編號'])
        setattr(order, 'material', row['材料'])
        setattr(order, 'color', row['顏色'])
        setattr(order, 'client', row['出貨客戶'])
        setattr(order, 'parting', row['分模'])
        setattr(order, 'ft_fixed', row['模修'])
        
       
        
        op_id = row['作業號碼']
        op_t = float(row['負荷(H)'])*3600

        op = Operation(order_id, op_id, op_t)
        setattr(op, 'pc_name', row['製程代號'])
        setattr(op, 'op_name', row['站點代號'])
        setattr(op, 'op_belongto', row['站點歸屬'])
        setattr(op, 'mcg_id', row['工作中心'])
        setattr(order, 'next_mcg_id', row['下工作中心'])
        return order, op
    
    orders_dict = {}
    
    for idx, row in wo_route_table.iterrows():
        order,op = retrieve(row)
        if op.order_id in orders_dict:
            order = orders_dict[op.order_id]
            order.op_list.append(op)
        else:
            orders_dict[op.order_id] = order
            order.op_list.append(op)

    return orders_dict

    
# =============================================================================
# 2.WIP
# =============================================================================

def create_wip_orders(wip, route_bom, CURRENTTIME, wip_order_DD):
    def get_rest_operation_data(pd_id, layer, op_id):
        #符合wip當前工站的route
        specific_row = route_bom[(route_bom['pd_id'] == pd_id)
                                        &(route_bom['layer'] ==layer)
                                        &(route_bom['op_id'] ==op_id)
                                        ]
        #TODO 若大於0 拋錯
        if specific_row.shape[0]>0:            
            sq_idx = specific_row['sq_idx'].values[0]
            rest_routes = route_bom[(route_bom['pd_id'] == pd_id)
                                            &(route_bom['sq_idx']>=sq_idx)
                                            ]
            return rest_routes
        return pd.DataFrame()

    wip_orders = {}
    for order_id, wip_data in wip.items():
        pd_id = wip_data['virtual_pd_id']
        layer = wip_data['layer']
        
        ES = 0
        DD = wip_order_DD[order_id]
        wip_order = Order(order_id, pd_id, ES, DD)
        setattr(wip_order, 'sheet', wip_data['sheet'])
        setattr(wip_order, 'pcs', wip_data['pcs'])
        op_id = wip_data['op_id']
        rest_op_data = get_rest_operation_data(pd_id, layer, op_id)
        if rest_op_data.shape[0]>0:
            wip_op_list = []
            for idx, op_data in rest_op_data.iterrows():
                idx = op_data['idx']
                op_id = op_data['op_id']
                op_t = op_data['op_t']
                op_t = ra.randint(100, 200)
                wip_op = Operation(idx, op_id, op_t)
                # TODO 之後可以用dictionary將額外欄位用append_special生成物件
                pd_id = op_data['pd_id']
                setattr(wip_op, 'pd_id', pd_id)
                setattr(wip_op, 'layer', layer)
                
                setattr(wip_op, 'order_id', order_id)
                wip_op_list.append(wip_op)
            setattr(wip_order, 'op_list', wip_op_list)
        
            wip_orders[order_id] = wip_order
    return wip_orders
# def classify_wip(wip, CURRENTTIME):
#     for idx, row in wip.iterrows():
#         wip_data = retrieve(row)
#         #在機群附近,凍結其以內的不動工序結果。凍結其之外的變成虛擬wip_order, 照原本排程排上甘特圖
#         #wip_order生成
#         freezed_time = CURRENTTIME+ datetime.timedelta(days = 3)
#         if pd.isna(wip_data['on_machine']):
#             #wip的開始時間為當下排程時間
#             wip_data['ES'] = CURRENTTIME
#             #wip的交期依據原工單交期
#             wip_data['DD'] = get_order_DD(wip_data['order_id'])
#             #初始工站等於wip當下工站
#             wip_data['init_op'] = wip_data['op_id']
#             wip_order = Order(wip_data)
#             wip_order_list.append(wip_order)
#         # #已在機台上加工一段時間, 形成wip_block, wip_bucket
#         # else:
#         #     order_id = wip_data['order_id']
#         #     op_id = wip_data['op_id']
#         #     start = CURRENTTIME
#         #     end = wip_data['pcs']*get_time(route)
#     return     
# =============================================================================
# 3.MachineGroup
# =============================================================================
  # def create_mc(mcg_table):
  #       mc_dict = {}
  #       unique_mc_list = mcg_table['機台編號'].unique()
  #       for mc_id in unique_mc_list:
  #           mc = Machine(mc_id)
  #           mc_dict[mc_id] = mc
  #       return mc_dict
  #   def create_mcg(mcg_table):
  #       mcg_dict = {}
  #       for idx, row in mcg_table.iterrows():
  #           mcg_id = mcg_table['機台類型編號']
  #           if mcg_id not in mcg_dict:
  #               mcg = MachineGroup(mcg_id)
  #               mcg_dict[mc_id] = mcg
            
  #       for mcg_id in unique_mc_list:
  #           mcg = MachineGroup(mcg_id)
  #           mcg_dict[mcg_id] = mcg
def extend_mcg_table(mcg_table, route_bom):
    unique_op_list = route_bom['op_id'].unique().tolist()
    #TODO 注意 刪掉是因為原始資料有 原本不想用虛擬資料替代，之後可以拔掉
    # unique_op_list.remove('A20')
    rows_list = []
    for op_id in unique_op_list:
        #機群數
        is_parallel = ra.choice(['Y', 'N'])
        for layer in range(6):
            Nmcg = 2
            Nmc = ra.randint(1, 2)*2
            for i in range(Nmcg):
                mcg_name = str(op_id)+'-機群%d'%i
                mcg_id = str(op_id)+'-mcg%d'%i
                
                for j in range(Nmc):
                    mc_data = {}
                    mc_name = str(op_id)+'-機台%d'%j
                    mc_id = str(op_id)+'-mc%d'%j
                    mc_data['工作中心'] = op_id
                    mc_data['層別'] = layer
                    mc_data['機台類型名稱'] = mcg_name
                    mc_data['機台類型編號'] = mcg_id
                    mc_data['機台名稱'] = mcg_id
                    mc_data['機台編號'] = mc_id
                    mc_data['可拆單'] = is_parallel
                    rows_list.append(mc_data)
    df = pd.DataFrame(rows_list) 
    mcg_table = pd.concat([df, mcg_table])
    
    return mcg_table

def create_mcg_dict(mcg_table):
    #將data資料轉出來
    #建立一個工作中心資料的dictionary
    op_data_dict = {}
    #for迴圈機群情境表每一個row和indx:
    for index, row in mcg_table.iterrows():
        #定義mcg_id為機台類型名稱、工作中心key
        op_key = row['工作中心']
        mcg_name = row['機台類型名稱']
        #定義row data分別為每一行的欄位內容
        row_data = {'mcg_name':row['機台類型名稱'],
                    'mcg_id':row['機台類型編號'],
                    'mc_id':row['機台編號']
                    }
        #if op_key沒有在op_data_dict裡面則將該op_key加入新增dict{}，並將該row data一同加入
        if op_key not in op_data_dict:
            op_data_dict[op_key] = {}
            op_data_dict[op_key][mcg_name] = [row_data]
        else:
            #else 機群mgc_id不在op_data_dict[op_key]裡則將該mgc_id加入新增lsit[]，無論有無包含mgc_id都會將row data一同加入
            if mcg_name not in op_data_dict[op_key]:
                op_data_dict[op_key][mcg_name] = []
            op_data_dict[op_key][mcg_name].append(row_data)
    #建立工作中心、機群、機台的dictionary
    op_dict = {}
    mcg_dict = {}
    mc_dict = {}
    #將op_data_dict裡每個item的key和mcg_data跑for迴圈，每個key建立一個list
    for key, mcg_data in op_data_dict.items():
        op_dict[key] = []
        #將mc_data每個item的mgc_id和mc_data_list跑for迴圈，mcg定義為機群物件且會有一個mc_list
        for mcg_name, mc_data_list in mcg_data.items():
            mcg = MachineGroup(mcg_name)
            #將mc_data_list每個mc_data跑for迴圈，mc定義為機台物件並新增屬性mcg_name與id
            for mc_data in mc_data_list:
                mc = Machine(mc_data['mc_id'])
                setattr(mcg, 'mcg_name', mc_data['mcg_name'])
                setattr(mcg, 'id', mc_data['mcg_id'])
                #機群物件裡的mc_list加入該mc物件
                mcg.add_mc(mc)
                #if該mc物件id不在mc_dict裡則加入該mc物件id到機台diict裡且放該mc物件
                if mc.id not in mc_dict:
                    mc_dict[mc.id] = mc
            #無論該mc物件id是否在mc_dict裡都要append機群id進去op_dict[key]
            op_dict[key].append(mcg.id)
            #if機群物件id不在mcg_dict裡則加入該機群物件id到機群diict裡且放該mcg物件
            if mcg.id not in mcg_dict:
                print(mcg.id)
                mcg_dict[mcg.id] = [mcg] 
    return op_dict, mcg_dict, mc_dict


# def create_process_data(mcg_table):
#     op_layer_data_dict = {}
#     for idx, row in mcg_table.iterrows():
#         mcg_id = row['機台類型名稱']
#         op_layer_key = row['工作中心']+"-"+str(int(row['層別']))
#         row_data = {'mcg_name':row['機台類型名稱'],
#                     'mcg_id':row['機台類型編號'],
#                     'mc_id':row['機台編號'],
#                     'is_parallel':row['可拆單'],
#                     'man_mc_ratio':row['人機比值'],
#                     'para_num':row['對打數量']
#                     }
#         if op_layer_key not in op_layer_data_dict:
#             op_layer_data_dict[op_layer_key] = {}
#             op_layer_data_dict[op_layer_key][mcg_id] = [row_data]
#         else:
#             if mcg_id not in op_layer_data_dict[op_layer_key]:
#                 op_layer_data_dict[op_layer_key][mcg_id] = []
#             op_layer_data_dict[op_layer_key][mcg_id].append(row_data)
#     op_layer_dict = {}
#     mcg_dict = {}
#     mc_dict = {}
    
    
#     #將op_data_dict裡每個item的key、mcg_data跑for迴圈
#     for key, mcg_data in op_layer_data_dict.items():
#         op_layer_dict[key] = []
#         for mcg_id, mc_data_list in mcg_data.items():
#             mcg = MachineGroup(mcg_id)
#             for mc_data in mc_data_list:
#                 mc = Machine(mc_data['mc_id'])
#                 setattr(mcg, 'mcg_name', mc_data['mcg_name'])
#                 setattr(mcg, 'id', mc_data['mcg_id'])
#                 setattr(mc, 'is_parallel', mc_data['is_parallel'])
#                 setattr(mc, 'man_mc_ratio', mc_data['man_mc_ratio'])
#                 setattr(mc, 'para_num', mc_data['para_num'])
#                 mcg.add_mc(mc)
#                 if mc.id not in mc_dict:
#                     mc_dict[mc.id] = mc
#             op_layer_dict[key].append(mcg.id)
#             if mcg.id not in mcg_dict:
#                 mcg_dict[mcg.id] = [mcg]                    
#     return op_layer_dict, mcg_dict, mc_dict
    
def get_time():
    time = ra.randint(30, 50)
    return time

def get_order_DD(order_id):
    return ra.randint(3000, 5000)

def get_rest_operations(pd_id, layer_num):
    pass

# def create_wip_bucket(wip, route_bom, CURRENTTIME):
#     def get_rest_operation_data(pd_id, layer, op_id):
#         #符合wip當前工站的route
#         specific_row = route_bom[(route_bom['pd_id'] == pd_id)
#                                         &(route_bom['layer'] ==layer)
#                                         &(route_bom['op_id'] ==op_id)
#                                         ]
#         if specific_row.shape[0]>0:            
#             sq_idx = specific_row['sq_idx'].values[0]
#             rest_routes = route_bom[(route_bom['pd_id'] == pd_id)
#                                             &(route_bom['sq_idx']>=sq_idx)
#                                             ]
#             return rest_routes
#         return 
#     #Never Change
#     wip_order_list = []
#     for order_id, wip_data in wip.items():
#         pd_id = wip_data['virtual_pd_id']
#         layer = wip_data['layer']
#         op_id = wip_data['op_id']
        
#         rest_op_data = get_rest_operation_data(pd_id, layer, op_id)
#         for idx, op_data in rest_op_data.iterrows():
#             wip_op = Operation()
            
# =============================================================================
#         #在機群附近,凍結其以內的不動工序結果。凍結其之外的變成虛擬wip_order, 照原本排程排上甘特圖
#         #wip_order生成
#         if pd.isna(wip_data['on_machine']):
#             #wip的開始時間為當下排程時間
#             wip_data['ES'] = CURRENTTIME
#             #wip的交期依據原工單交期
#             wip_data['DD'] = get_order_DD(wip_data['order_id'])
#             #初始工站等於wip當下工站
#             wip_data['init_op'] = wip_data['op_id']
#             wip_order = Order(wip_data)
#             wip_order_list.append(wip_order)
#         #已在機台上加工一段時間, 形成wip_block, wip_bucket
#         else:
#             order_id = wip_data['order_id']
#             op_id = wip_data['op_id']
#             start = CURRENTTIME
#             end = wip_data['pcs']*get_time(route)        
# =============================================================================

        


def create_orders_operations(order_data, route_table, CURRENTTIME):
    '''
    回傳所有工單(Order)的字典查詢表、所有工序(Operation)的物件
    '''
    orders_dict = {}
    all_op_list = []
    for i in range(len(order_data)):
        order_id = order_data['order_id'].iloc[i]
        pd_id = order_data['pd_id'].iloc[i]
        total_qty = order_data['qty'].iloc[i]
        qty_list = seperate_demand(total_qty)
        ES_date = order_data['ES'].iloc[i]
        ES_date-=datetime.timedelta(hours = 8)
        ES = ES_date.timestamp() - CURRENTTIME.timestamp()
        # ES_list = get_ES_list(ES, qty_list)
        DD_date = order_data['DD'].iloc[i]
        DD_date-=datetime.timedelta(hours = 8)
        DD = DD_date.timestamp() - CURRENTTIME.timestamp()
        op_list = get_operations(pd_id, order_id, route_table)
        all_op_list.extend(op_list)
        orders_dict[order_id] = Order(order_id, op_id, ES, DD)
    return orders_dict, all_op_list

#TODO
def get_ES_list(ES, qty_list):
    ES_list = [ES]*len(qty_list)
    return ES_list
        
#TODO
#未來改成MTQ
def seperate_demand(total_qty):
    molecular = 10
    quotient = total_qty // molecular
    remainder = total_qty % molecular
    qty_list = [molecular]*quotient
    qty_list.append(remainder)
    return qty_list

# def get_operations(pd_id, order_id, route_table):
#     '''
#     獲取某工單的所有operations
#     '''
#     op_data = []
#     for idx, row in route_table.iterrows():
#         if row['pd_id'] == pd_id:
#             op_data.append(row)
#     op_data = pd.DataFrame(op_data)
#     op_list = []
#     for i in range(len(op_data)):
#         pd_id = route_table['pd_id'].iloc[i]
#         op_id = route_table['op_id'].iloc[i]
#         su_t = route_table['su_t'].iloc[i]
#         op_t = route_table['op_t'].iloc[i]
#         mcg_id = route_table['mc_group_id'].iloc[i]
#         next_op = route_table['next_op'].iloc[i]
#         is_crr = route_table['is_crr'].iloc[i]
#         is_claw = route_table['is_claw'].iloc[i]
#         ft_id = route_table['ft_id'].iloc[i]
#         op = Operation(pd_id, order_id, op_id, su_t, op_t, mcg_id, next_op, is_crr, is_claw, ft_id)
#         op_list.append(op)
        
#     return op_list

def create_rs_dict(pc_list):
    mcg_dict = {}
    ft_dict = {}
    for pc in pc_list:
        for mcg in pc.mcg_list:
            
            mcg_dict[mcg.id] = mcg
            for ft in mcg.ft_list:
                ft_dict[ft.id] = ft
    return mcg_dict, ft_dict
    
    
    
    
    
    
    