# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 17:45:42 2021

@author: RoyTseng
"""
import random as ra

from VirtualFactory.Machine import Machine, MachineGroup


class Process:
    def __init__(self, pc_id):
        self.id = pc_id
        self.mcg_list = []
        
    def add_mc_group(self, mcg_list):
        for mcg in mcg_list:
            self.mcg_list.append(mcg)    
        

def gen_pc_list(Npc:6, Rmcg:(3,5), Rmc:(2,3), Rwf:(0,2)):
    '''
    Parameters
    ----------
    Npc : 6
        設定製程生成數
    Rmc : (3,5)
        設定各製程機群亂數範圍
    Rmc : (2,3)
        設定各機台亂數範圍
    Rft : (0,2)
        設定各機台治具亂數範圍
    Rwf : (0,2)
        設定各機台所需人力亂數範圍

    Returns
    -------
    pc_list : TYPE
        DESCRIPTION.
    '''
    #Process Number
    pc_list = []
    mcg_counter = 0
    mc_counter = 0
    ft_counter = 0
    for i in range(Npc):
        Nmcg = ra.randint(Rmcg[0], Rmcg[1])
        mcg_list = [MachineGroup(Nmc=ra.randint(2,3)) for i in range(Nmcg)]
        for mcg in mcg_list:
            mcg.id = "mcg_%03d" % mcg_counter
            # print(mcg.id)
            mcg_counter+=1
            for mc in mcg.mc_list:
                mc.id = "mc_%03d" % mc_counter
                mc_counter+=1
            for ft in mcg.ft_list:
                ft.id = "ft_%03d" % ft_counter
                ft_counter+=1
        pc_id = 'pc %03d' % i
        pc = Process(pc_id)
        pc.add_mc_group(mcg_list)
        pc_list.append(pc)
    return pc_list

# mcg_list = [MachineGroup(Nmc = ra.randint(2,5), Nft = ((0,2))) for i in range(5)]
# pc_list = gen_pc_list(Npc=6, Rmcg=(3,5), Rmc=(2,3), Rwf=(0,2)) 

