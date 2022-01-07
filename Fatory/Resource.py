# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 16:09:02 2021

@author: DALab
"""
import abc
from APS.Block import Block
class Resource(abc.ABC):
    def __init__(self):
        self.id = ''
        self.ES = 0
        
        self.block_list = []
        self.block_size = 0

    # def get_available_block(self):
    #     pass
    # def add_block(self, new_load):
    #     block_list = self.block_list
    #     ES = max(self.ES, new_block.ES)
    #     if len(block_list)==1:
    #         self.append_block(new_block, ES)
            
    def append_block(self,new_block,release_time):
        new_block.start = release_time
        new_block.end = new_block.start + new_block.duration

        
    # self.loads_list.append(new_load)  
    def reset(self, CURRENTTIME):
        self.ES = 0
        
        
    def __lt__(self, other):
        return self.ES < other.ES
    
    def __str__(self):
        resource_data = 'ID:'+ self.id+'\n'
        resource_data += 'ES:'+ str(self.ES)+'\n'
        return resource_data
        