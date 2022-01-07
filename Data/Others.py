        
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 14:44:41 2021

@author: DALab
"""
import datetime
import random as ra 
import numpy as np
from APS.Block import Block
from APS.Bucket import Bucket
from Decode import dispatch
def create_forbidden_info(PPAD, CURRENTTIME):
    forbidden_buckets = []
    forbidden_info = {}
    for idx, row in PPAD.iterrows():
        start = datetime.datetime.strptime(str(row['開始時間']), '%Y-%m-%d %H:%M:%S')
        start = start.timestamp()-CURRENTTIME
        end = datetime.datetime.strptime(str(row['結束時間']), '%Y-%m-%d %H:%M:%S')
        end = end.timestamp()-CURRENTTIME
        reason = row['備註']
        block = Block(reason, start, end)
        bucket = Bucket(reason, start, end)
        setattr(bucket,'mc_name', row['機台名稱'])
        
        bucket.block_list = [block]
        forbidden_buckets.append(bucket)
        if row['機台名稱'] not in forbidden_info:
            forbidden_info[row['機台編號']] = [bucket]
        else:
            forbidden_info[row['機台編號']].append(bucket)
    return forbidden_info

def decode_forbidden(forbidden_info, schedule, mc_dict):
    for mc_id, bucket_list in forbidden_info.items():
        #TODO 目前有些機台是沒有相關資料的 'PTH101001'
        if mc_id in schedule:
            mc = schedule[mc_id]
            for bucket in bucket_list: 
                mc.bucket_list.append(bucket)
            schedule[mc_id] = mc 
    return schedule

def get_DD_for_wip(wip):
    DD = datetime.datetime.strptime('2021/4/3 12:00 AM', '%Y/%m/%d %I:%M %p')
    wip_DD_dict = {}
    
    for key, wip_data in wip.items():
        DD = DD+datetime.timedelta(hours = ra.randint(5, 12))
        wip_order_id = wip_data['order_id']
        wip_DD_dict[wip_order_id] = DD
    return wip_DD_dict

def load_machines(mc_dict):
    schedule = {}
    for mc_id, mc in mc_dict.items():
        schedule[mc_id] = mc
    return schedule 

def decode_wip(data, forbidden_schedule):
    wip_schedule = forbidden_schedule
    for key, order in data.wip_orders.items():
        op_list = order.op_list
        for op in op_list:
            mcg_id_list = data.op_layer_mcg_dict[str(op.id)+'-'+str(op.layer)]
            mcg_list = []
            for mcg_id in mcg_id_list:
                mcg = data.mcg_dict[mcg_id][0]
                mcg_list.append(mcg)
            wip_schedule = dispatch(wip_schedule, order, data, op, mcg_list)
    return wip_schedule
