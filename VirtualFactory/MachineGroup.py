# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 13:20:34 2021

@author: DALab
"""
import random as ra
class Machine:
    def __init__(self, Nft, Nwf):
        self.id = None
        self.Nft = Nft
        self.ft_list = []
        self.Nwf = Nwf

class MachineGroup:
    def __init__(self):
        self.id = None
        self.mc_list = []
        self.mc_heapq = []
    
    def add_machine(self, mc):
        self.mc_list.append(mc)
        hq.heappush(self.mc_heapq, mc)
        
    def get_earliest_available_machine(self):
        return hq.nsmallest(1,self.mc_heapq)[0]


# #機群數
# Nmg = 5
# mg_list = []
# for i in range(Nmg):
#      mg = MachineGroup()
#      Nmc = ra.randint(2,5)
#      for j in range(Nmc):
#          mg.add_machine(Machine(ra.randint(1,3), bool(ra.getrandbits(1))))
#      mg_list.append(mg)