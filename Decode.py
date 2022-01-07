# -*- coding: utf-8 -*-
"""
Title: Job Shop Scheduling Module
Version: 0.1
Author: Kuan-Chen Tseng k.c.tseng@ie.nthu.edu.tw
Copyright: Belongs to DAlab Solutions x Associates Co.,Ltd.
"""

import random as ra
import numpy as np
from APS.Block import Block
from APS.Bucket import Bucket
import copy
#TODO 設定只排特定工單
def set_orders(order_id_list):
    orders_list = []
    # op_list3 = []
    # op_list = data.orders['wo_000'].op_list
    # op_list2 = data.orders['wo_009'].op_list
    # op_list3.extend(op_list2)
    return orders_list
#解碼
#回傳實際可加工工序
def get_available_operation(data, sq_idx):
    #tmp_op = 演算法欲排的工序
    tmp_op = data.all_op_list[sq_idx]
    #order_code = 該工序所對應的工單編號 (e.g., 15260898
    order_id = tmp_op.order_id
    #op = 實際上可加工的工序
    op = data.orders_dict[order_id].get_target_op()
    data.orders_dict[order_id].target_next_op()
    return op

def decode(particle, data):
    schedule = data.reset()
    seq = np.argsort(particle)
    counter = 0 
    for idx, sq in enumerate(seq):
        op = get_available_operation(data, sq)
        order = data.orders_dict[op.order_id]
        mcg_id = op.mcg_id[:-2]
        counter+=1
        print(counter)
        mcg = data.mcg_dict[mcg_id]
        schedule = dispatch(schedule, order, data, op, mcg[0])
    return schedule

def dispatch(schedule, order, data, op, mcg):
    # TODO 之後由機台配適表決定機群(layer, station)
    #建立一個空的bucket:[]代表一個op
    bucket_list = formulate_buckets(order, op)
    if order.id ==7000554006:
        print(len(bucket_list))
    
    # bucket.block_list = [Block, Block...Block] 前一個block結束時間

    ES = order.ES
    # # ES = max(order.ES, find_rs_ES())
    max_op_end = insert(schedule, ES, bucket_list, mcg)
    # order.ES = max_op_end
    return schedule

#機台挑選
def mc_selection(info_list):
    best_mc_idx = 0
    #最小可開始時間min_ES = info_list第一個[0]最早可開始時間ES
    min_ES = info_list[0]['ES']
    #對所有mc_idx跑for迴圈，if機台ES小於min_ES則該機台就是最早可開始機台，最後回傳最早可排機台
    for mc_idx in range(len(info_list)):
        ES = info_list[mc_idx]['ES']
        if ES < min_ES:
            best_mc_idx = mc_idx
            min_ES = ES
    return best_mc_idx, info_list[best_mc_idx]

#插入(排程dictionary, 最早可開始時間, operation list, 機群)
def insert(schedule, ES, bucket_list, mcg):
    
    #宣告bucket最後結束時間 (為了order.ES=max_op_end)
    max_op_end = 0
    #在bucket list的每個bucket跑for迴圈
    for bucket in bucket_list:
        #宣告一個info_list是一個空list[]
        info_list = []
        #在機群物件裡的mc_list裡的每個mc物件跑for迴圈
        for mc in mcg.mc_list:
            #宣告mc = schedule dictionary裡的mc物件id
            mc = schedule[mc.id]
            #宣告slot_info = mc物件裡最好的最早開始時間ES,bucket物件可排區間duration
            slot_info = mc.get_best_slot_info(ES, bucket.duration)
            #再將最好的slot_info機台物件append進去info_list
            info_list.append(slot_info)
        #回傳從info_list中選出的最早可生產機台index和最好slot_info
        best_mc_idx, best_slot_info = mc_selection(info_list)
        #宣告diff=最好可生產機台的ES-bucket物件的開始時間
        diff = best_slot_info['ES'] - bucket.start
        #平移向量(有正負)
        bucket.move(diff)
        best_mc_id = mcg.mc_list[best_mc_idx].id
        best_mc = schedule[best_mc_id]
        best_mc.bucket_list.insert(best_slot_info['idx'], bucket)
        if bucket.end>max_op_end:
            max_op_end = bucket.end
    return max_op_end

def formulate_buckets(order, op):
    # TODO之後改由最大可拆單數量來平分
    def split(qty, para_num):
        bucket_length = []
        length = qty//para_num 
        bucket_length = [length for _ in range(para_num)]
        rest = qty%para_num 
        for i in range(rest):
            bucket_length[i]+=1
        return bucket_length
    # TODO 之後由機台配飾表決定機群
    bucket = Bucket(order.id, 0, 0)
    start = 0
    duration = 0 + op.op_t
    end = start + duration
    
    block = Block(order.id, start, end)
    bucket.add_block(block)
    # para_num = len(mcg.mc_list)
    # #TODO 目前By sheet拆單
    # bucket_length = split(order.sheet, para_num)
    # bucket_list = [Bucket(order.id, 0, 0) for _ in range(para_num)]
    # for idx, demand in enumerate(bucket_length):
    #     #TODO 之後改工時模式
    #     start = 0
    #     end = 200 + demand*20
    #     block = Block(order.id, start, end)
    #     setattr(block, 'op_id', op.id)
    #     bucket_list[idx].add_block(block)
    #     setattr(bucket_list[idx], 'op_id', op.id)
    return [bucket]