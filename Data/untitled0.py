# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 16:03:22 2021

@author: RoyTseng
"""
def split(qty, para_num):
    bucket_length = []
    length = qty//para_num 
    bucket_length = [length for _ in range(para_num)]
    rest = qty%para_num 
    for i in range(rest):
        bucket_length[i]+=1
    return bucket_length
