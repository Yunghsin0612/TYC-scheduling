# -*- coding: utf-8 -*-
"""
Title: Job Shop Scheduling Module
Version: 0.1
Author: Kuan-Chen Tseng k.c.tseng@ie.nthu.edu.tw
Copyright: Belongs to DAlab Solutions x Associates Co.,Ltd.
"""

from SSO.SSO import SSO
import random


#改寫初始解產生方式
def create_particle(data):
    return [random.randint(0,data['UB']) for _ in range(data['Nvar'])]

#改寫適應度函數
def cal_fit(solution, data):
    total = 0
    for i in range(data['Nvar']):    
        total+= solution[i]
    return total 

def step_wise_function(data, x, px, gbest, Cp, Cg, Cw):
    for var, value in enumerate(x):
        rnd_dot = random.random()
        if(rnd_dot < Cp):
            x[var] = px[var]
        if(rnd_dot < Cg):
            x[var] = gbest[var]
        elif(rnd_dot < Cw):
            continue
        else:
           x[var] = random.randint(0,data['UB'])
    return x
#自行設定資料格式
data = {'Nvar':10, 'UB':5} 
#SSO(data, 母群體個數, 世代數)
sso = SSO(data,10,100)
#替代原本function
sso.create_particle = create_particle
sso.cal_fit = cal_fit
sso.step_wise_function = step_wise_function
sso.run()
