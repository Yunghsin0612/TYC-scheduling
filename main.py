# -*- coding: utf-8 -*-
"""
Title: APS Module
Version: 0.1
Author: Kuan-Chen Tseng k.c.tseng@ie.nthu.edu.tw
Copyright: Belongs to DAlab Solutions x Associates Co.,Ltd.
"""
import datetime
import sys
import os
import cProfile
#VirtualFactory
from VirtualFactory.Customer import Customer
from VirtualFactory.FactoryBuilder import Factory

#Data
# from Data.FakeData import Data
from Data.Data import Data

#APS
sys.path.append(os.getcwd()+'/最佳化搜尋演算法模組')
from SSO.SSO import SSO
from APS.Gantt import print_gantt
from Decode import decode
from SSO_override import create_particle, cal_fit, step_wise_function
# from Data.Others import decode

def get_factory(CURRENTTIME):
    ##創建虛擬工廠
    fac = Factory(CURRENTTIME)
    #TODO 一人多單
    #接客數, 產生虛擬客戶(目前為一人一單)
    Ncust = 40
    cust_list = [Customer('cust_%03d'% i) for i in range(Ncust)]
    start = datetime.datetime.strptime('2020/1/1 8:00 AM', '%Y/%m/%d %I:%M %p')
    end = datetime.datetime.strptime('2020/1/3 1:30 PM', '%Y/%m/%d %I:%M %p')
    
    #設定客戶下單範圍
    purchase_horizon = (start, end)
    
    #將客戶給工廠，工廠將產品資訊交給客戶，客戶挑選產品，並制定交期
    fac.meet_customers(purchase_horizon, cust_list)
    
    #搜尋未來交期特定時間內的工單
    target_time = datetime.datetime.strptime('2020/1/3 1:30 PM', '%Y/%m/%d %I:%M %p')
    
    #決定開立工單的
    fac.set_target_orders(target_time)
    #工廠產生相關資料給APS
    return fac
    fac.gen_data()
# def test():
CURRENTTIME = datetime.datetime.strptime('2021/2/26 12:00 AM', '%Y/%m/%d %I:%M %p')
# fac = get_factory(CURRENTTIME)
# 傳入工廠物件，讓APS系統知道一些系統資訊
data = Data(CURRENTTIME)
# schedule = decode(data)
# Nvar:解的長度
sso_data = {'Nvar':len(data.all_op_list),'Nsol':1, 'Ngen':1, 'data':data}
# SSO(data, Nsol(母群體個數), Ngen(世代數))
sso = SSO(sso_data, sso_data['Nsol'], sso_data['Ngen'])
# #改寫初始解生成機制
sso.create_particle = create_particle
# sso.create_solutions = create_solutions
# #改寫適應度函數計算
sso.cal_fit = cal_fit
# #改寫更新機制
# sso.step_wise_function = step_wise_function
# #運算，並回傳近似最佳解
particle = sso.run()
# #解碼成甘特圖
schedule = decode(particle, data)
# #show gantt
print_gantt(schedule, CURRENTTIME)
# if __name__ == '__main__':

    
#     cProfile.run('test()',"output.dat")
#     import pstats
    
#     with open("output_time.txt","w") as f:
#         p = pstats.Stats("output.dat", stream=f)
#         p.sort_stats("time").print_stats()
        
#     with open("output_calls.txt","w") as f:
#         p = pstats.Stats("output.dat", stream=f)
#         p.sort_stats("calls").print_stats()
    