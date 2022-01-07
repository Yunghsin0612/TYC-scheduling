# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 23:44:09 2021

@author: RoyTseng
"""


import random
import numba as nb
import copy
from Algorithm.Tools import Tools 
from Algorithm.Particle import Particle

@nb.jit(nopython=True)
def step_wise_function(x, px, gbest, Cp, Cg, Cw):
    for var in range(len(x)):
        rnd_dot = random.random()
        if(rnd_dot < Cp):
            x[var] = px[var]
        elif(rnd_dot < Cg):
            x[var] = gbest[var]
        elif(rnd_dot < Cw):
            continue
        else:
           x[var] = random.randint(0, UB)
    return x
class SSO():
    def __init__(self, data, Nsol, Ngen):
        self.data = data
        self.Nsol = Nsol
        self.Ngen = Ngen
        self.Cp = 0.3
        self.Cg = 0.8
        self.Cw = 0.9
        self.X = []
        self.pX = []
        self.gbest_sol = None

    def run(self):
        self.init()
        self.gFs, self.gbest = self.update()
        sol = self.output()
        return sol
    def init(self):
        self.X = []
        for i in range(self.Nsol):
            solution = self.create_particle(self.data)
            fitness = self.cal_fit(solution, self.data)
            self.X.append(Particle(solution, fitness))    
        self.pX = copy.deepcopy(self.X)
        self.gbest_sol = Tools.find_best(self.X)
        
    def create_particle(self, data):
        return [random.randint(0, data['UB']) for _ in range(data['Nvar'])]
    
    def cal_fit(self, solution, data):
        total = 0
        for i in range(data['Nvar']):    
            total+= solution[i]*solution[i]
        return total

    def create_solutions(self):
        for sol in range(self.Nsol):
            self.X[sol] = self.create_particle(self.data)
        return self.X
    
    def update(self):
        gBest_value_list = []
        for gen in range(self.Ngen):
            for sol in range(self.Nsol):
                x = self.X[sol]
                px = self.pX[sol]
                gbest = self.pX[self.gbest_sol]
                Cp = self.Cp
                Cg = self.Cg
                Cw = self.Cw
                UB = 0
                x = step_wise_function(UB, x, px, gbest, Cp, Cg, Cw)
                x.F = self.cal_fit(x, self.data)
                if(Tools.compareTo(x.F,px.F)):
                    px.F = x.F
                    for var in range(len(px)):
                        px[var] =x[var]
                    if (Tools.compareTo(x.F,gbest.F)):
                        self.gbest_sol = sol
            gBest_value_list.append(gbest.F)
            print("gen:{}".format(gen)," fitness:{}".format(gbest.F))       
            # print("gen:{}".format(gen),gbest) 
        return gBest_value_list, self.pX[self.gbest_sol]

    def output(self):
        print('Approximate Optimal solution',self.gbest) 
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

# def step_wise_function(data, x, px, gbest, Cp, Cg, Cw):
#     for var, value in enumerate(x):
#         rnd_dot = random.random()
#         if(rnd_dot < Cp):
#             x[var] = px[var]
#         if(rnd_dot < Cg):
#             x[var] = gbest[var]
#         elif(rnd_dot < Cw):
#             continue
#         else:
#             x[var] = random.randint(0,data['UB'])
#     return x
def create_particle(data):
    return [random.randint(0, data['UB']) for _ in range(data['Nvar'])]
def create_solution():
    
data = {'Nvar':10, 'UB':2} 
#SSO(data, 母群體個數, 世代數)
X = create_solution()
