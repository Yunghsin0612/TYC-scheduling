# -*- coding: utf-8 -*-
"""
Title: Job Shop Scheduling Module
Version: 0.1
Author: Kuan-Chen Tseng k.c.tseng@ie.nthu.edu.tw
Copyright: Belongs to DAlab Solutions x Associates Co.,Ltd.
"""
import copy
class Tools:
    def FastEliteSelecting(sols):
        s_out=[copy.deepcopy(particle) for particle in sols]
        p_idx = 0
        while p_idx<len(s_out):
            p = s_out[p_idx]
            pop_p = False
            q_idx = 0
            while q_idx <len(s_out):
                pop_q = False
                q = s_out[q_idx]
                #p比q好
                if p.F[0] < q.F[0] and p.F[1] < q.F[1]\
                or p.F[0] <= q.F[0] and p.F[1] < q.F[1]\
                or p.F[0] < q.F[0] and p.F[1] <= q.F[1]:
                    s_out.pop(q_idx)
                    pop_q = True
                #q比p好
                elif p.F[0] > q.F[0] and p.F[1] > q.F[1]\
                or p.F[0] >= q.F[0] and p.F[1] > q.F[1]\
                or p.F[0] > q.F[0] and p.F[1] >= q.F[1]:
                    s_out.pop(p_idx)
                    pop_p=True
                    break
                if not pop_q:
                    q_idx+=1
            if not pop_p:
                p_idx+=1
        return s_out 

    def find_best(F):
        Max = F[0]
        idx =0
        for i in range(len(F)):
            if (Tools.compareTo(F[i],Max)):
                Max = F[i]
                idx = i
        return idx
    
    #最小值問題 就改成< 
    def compareTo(value0, value1):

        return value0<=value1

    
    def domain_modify(var, x):
        if x[var]> 1:
            x[var] = 1.0
        elif x[var]< 0:
            x[var] = 0.0
        return x
        