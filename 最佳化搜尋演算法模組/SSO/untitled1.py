# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 23:58:51 2021

@author: RoyTseng
"""
import numba as nb
import time
x = [10]
@nb.jit('int64[:](int64[:])')
def loop2(x):
    for i in range(100):
        for j in range(1000):
            x[0]+=j
            print(x[0])
    return x 
st = time.time()
x = loop2(x)
ed= time.time()
print('time:',ed-st)

