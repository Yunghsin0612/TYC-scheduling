# -*- coding: utf-8 -*-
"""
Title: Job Shop Scheduling Module
Version: 0.1
Author: Kuan-Chen Tseng k.c.tseng@ie.nthu.edu.tw
Copyright: Belongs to DAlab Solutions x Associates Co.,Ltd.
"""
import random
import math
# from Decode import decode
import numba as nb
from Decode import decode

#Random-key
def create_particle(sso_data):

    particle = []
    Nvar = sso_data['Nvar']
    for i in range(Nvar):
        particle.append(random.random())
    return particle

# def create_solutions(sso_data):
#     print('hi')
#     X = []
#     for i in range(sso_data['Nsol']):
#         pass
#     Nvar = sso_data['Nvar']
#     for i in range(Nvar):
#         particle.append(random.random())
#     return particle



#計算適應值
def cal_fit(particle, sso_data):
    def cal_makespan(schedule):
        makespan = 0
        for mc_id, mc in schedule.items():
            for bucket in mc.bucket_list:
                if bucket.end>makespan:
                    makespan = bucket.end
        return makespan
    #計算負荷平衡率
    def cal_balance(schedule):
        balance = 1
        return balance
        #計算lateness, N delay_job
    def cal_delay(data, schedule):
        order_end = {}
        for mcg_id, mcg in schedule.items():
            for mc in mcg.mc_list:
                for bucket in mc.bucket_list:
                    order_end[bucket.order_id] = bucket.end
        #cal_lateness
        Ndelay = 0
        lateness_sum = 0 
        for key, value in order_end.items():
            if key !='WIP':
                lateness = order_end[key] - data.orders_dict[key].DD
                lateness_sum += abs(lateness)
                if lateness>0:
                    Ndelay+=1
        return lateness_sum, Ndelay
    data = sso_data['data']
    schedule = decode(particle, data)
    # print(schedule[0])
    #計算總完工時間
    # makespan = cal_makespan(schedule)
    # lateness_sum, Ndelay = cal_delay(data, schedule)
    # balance = cal_balance(schedule)
    
    # w1 = 0.6
    # w2 = 0.4
    fitness = 1
    # w1*makespan+w2*balance
    return fitness
#更新機制(numba)
# @nb.jit(nopython=True)
# def step_wise_function(UB, x, px, gbest, Cp, Cg, Cw):
#     for var in range(len(x)):
#         rnd_dot = random.random()
#         if(rnd_dot < Cp):
#             x[var] = px[var]
#         elif(rnd_dot < Cg):
#             x[var] = gbest[var]
#         elif(rnd_dot < Cw):
#             continue
#         else:
#             x[var] = random.random()
#     return x

#連續型更新機制iSSO
def step_wise_function(data, x, px, gbest, Cp, Cg, Cw):
    u =  1/2*data['Nvar']
    Cr = 0.4
    Cg = 0.75
    for var, value in enumerate(x):
        rnd_dot = random.random()
        rnd_dot2 = rnd_dot-0.5
        if(rnd_dot < Cr or x[var] == gbest[var]):
            x[var]+=rnd_dot2*u
        if(Cr < rnd_dot < Cg and x[var] != gbest[var]):
            x[var] = gbest[var]+rnd_dot2*u
        if(x[var] != gbest[var] and Cg<rnd_dot<1):
            x[var] += (x[var]-gbest[var])*rnd_dot2
    return x
