# -*- coding: utf-8 -*-
"""
Title: Job Shop Scheduling Module
Version: 0.1
Author: Kuan-Chen Tseng k.c.tseng@ie.nthu.edu.tw
Copyright: Belongs to DAlab Solutions x Associates Co.,Ltd.
"""

class Bucket:
    #Bucket Class宣告初始化物件屬性
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
        self.duration = end - start 
        self.block_list = []
        self.length = 0
    
    #新增block進去的function
    def add_block(self, block):
        #i bucket長度=0時:bucket開始/結束時間=block開始/結束時間
        if self.length == 0:
            block.start = 0
            self.start = block.start
            block.end = block.start + block.duration
            self.end = block.end
        #else bucket長度不=0時:
        else:
            last_block = self.block_list[-1] #last_block定義為目前block_list的前一者
            block.start = last_block.end #block開始時間=前一個block結束時間
            block.end = block.start + block.duration #block結束時間=開始時間+一個block加工區間時間
            self.end = block.end #bucket結束時間=block結束時間
        #將目前的block_list加上一個block
        self.block_list.append(block)
        self.duration = self.end - self.start
        self.length+=1 #計算bucket裡block數量
        
    #block跟著bucket移動更新時間    
    def __update_blocks_time(self, time):
        for block in self.block_list:
            block.move(time)
    
    #bucket移動更新開始/結束時間         
    def move(self, time):
        self.start+=time
        self.end+=time
        self.__update_blocks_time(time)

    def __lt__(self, other):
        return self.end<other.end
    
    def get_duration(self):
        return self.end-self.start
    
    def __repr__(self):
        data = "Bucket "+str(self.name)+"("+str(self.start)+", "+str(self.end)+")"+'\n'
        data+= ":"+str(self.block_list)+"\n"
        return data