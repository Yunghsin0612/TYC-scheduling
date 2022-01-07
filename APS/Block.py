# -*- coding: utf-8 -*-
"""
Title: Job Shop Scheduling Module
Version: 0.1
Author: Kuan-Chen Tseng k.c.tseng@ie.nthu.edu.tw
Copyright: Belongs to DAlab Solutions x Associates Co.,Ltd.
"""

class Block:
    def __init__(self,name, start, end):
        self.name = name
        self.start = start
        self.end = end
        self.duration = end - start
        
    def move(self, time):
        self.start+=time
        self.end+=time
  
    def __lt__(self, other):
        return self.end<other.end
    
    def get_duration(self):
        return self.end-self.start
    
    def __str__(self):
        return "Block("+str(self.start)+", "+str(self.end)+")"
    
    def __repr__(self):
        return "Block("+str(self.start)+", "+str(self.end)+")"
