# -*- coding: utf-8 -*-
"""
Title: Job Shop Scheduling Module
Version: 0.1
Author: Kuan-Chen Tseng k.c.tseng@ie.nthu.edu.tw
Copyright: Belongs to DAlab Solutions x Associates Co.,Ltd.
"""
import time
import random
import numpy as np
import numba as nb
import copy
from Algorithm.Tools import Tools 
from Algorithm.Particle import Particle
@nb.jit(nopython=True)
def step_wise_function(UB, x, px, gbest, Cp, Cg, Cw):
    for var in range(len(x)):
        rnd_dot = random.random()
        if(rnd_dot < Cp):
            x[var] = px[var]
        elif(rnd_dot < Cg):
            x[var] = gbest[var]
        elif(rnd_dot < Cw):
            continue
        else:
           x[var] = random.random()
    return x
# # @nb.jit(nopython=True)
# def step_wise_function(data, x, px, gbest, Cp, Cg, Cw):
#     u =  1/2*data['Nvar']
#     Cr = 0.4
#     Cg = 0.75

#     for var, value in enumerate(x):
#         rnd_dot = random.random()
#         rnd_dot2 = rnd_dot-0.5
#         if(rnd_dot < Cr or x[var] == gbest[var]):
#             x[var]+=rnd_dot2*u
#         if(Cr < rnd_dot < Cg and x[var] != gbest[var]):
#             x[var] = gbest[var]+rnd_dot2*u
#         if(x[var] != gbest[var] and Cg<rnd_dot<1):
#             x[var] += (x[var]-gbest[var])*rnd_dot2
#     return x
class SSO():
    def __init__(self, data, Nsol, Ngen):
        self.data = data
        self.Nsol = Nsol
        self.Ngen = Ngen
        self.Cp = 0.5
        self.Cg = 0.83
        self.Cw = 0.93
        
        self.X = None
        self.F = None
        self.pX = None
        self.pF = None
        self.gbest_sol = None

    def run(self):
        self.init()
        self.gFs, self.gbest = self.update()
        sol = self.output()
        return sol
    
    def init(self):
        self.X = []
        self.F = []
        for i in range(self.Nsol):
            particle = self.create_particle(self.data)
            self.X.append(particle)
            fitness = self.cal_fit(particle, self.data)
            self.F.append(fitness)
        self.X = np.array(self.X)
        self.F = np.array(self.F)
        self.pX = copy.deepcopy(self.X)
        self.pF = copy.deepcopy(self.F)
        self.gbest_sol = Tools.find_best(self.F)
        
    def create_particle(self, data):
        return np.random.random_sample(data['Nvar'], )
        
    def cal_fit(self, solution, data):
        total = 0
        for i in range(len(solution)):    
            total+= solution[i]*solution[i]
        return total
    
    def create_solutions(self, data):
        for sol in range(self.Nsol):
            self.X[sol] = self.create_particle(self.data)
        return self.X
    
    def update(self):
        gBest_value_list = []
        # data = {}
        for gen in range(self.Ngen):
            for sol in range(self.Nsol):
                x = self.X[sol]
                px = self.pX[sol]
                gbest = self.pX[self.gbest_sol]
                Cp = self.Cp
                Cg = self.Cg
                Cw = self.Cw
                
                x = step_wise_function(0, x, px, gbest, Cp, Cg, Cw)
                self.F[sol]= self.cal_fit(x, self.data)
                if(Tools.compareTo(self.F[sol], self.pF[sol])):
                    self.pF[sol] = self.F[sol]
                    for var in range(len(px)):
                        px[var] = x[var]
                    if (Tools.compareTo(self.F[sol],self.pF[self.gbest_sol])):
                        self.gbest_sol = sol
            gBest_value_list.append(self.pF[self.gbest_sol])
            print("gen:{}".format(gen)," fitness:{}".format(self.pF[self.gbest_sol]))       
            # print("gen:{}".format(gen),gbest) 
        return gBest_value_list, self.pX[self.gbest_sol]

    def output(self):
        # print('Approximate Optimal solution',self.gbest) 
        return self.gbest


# =============================================================================
# 測試區
# =============================================================================

# #改寫初始解產生方式
# def create_particle(data):
#     return [random.randint(0,data['UB']) for _ in range(data['Nvar'])]

# #改寫適應度函數
# def cal_fit(solution, data):
#     total = 0
#     for i in range(data['Nvar']):    
#         total+= solution[i]
#     return total 

# data = {'Nvar':100, 'UB':2} 
# #SSO(data, 母群體個數, 世代數)
# sso = SSO(data,100,600)
# print(sso.Cw)
# #替代原本function
# # sso.create_particle = create_particle
# # sso.cal_fit = cal_fit
# # sso.step_wise_function = step_wise_function
# st = time.time()
# sol = sso.run()
# ed= time.time()
# print('time:',ed-st)

