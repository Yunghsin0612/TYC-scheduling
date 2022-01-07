# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 13:20:34 2021
@author: DALab
"""
import random as ra
import heapq as hq
from VirtualFactory.Resource import Resource
from VirtualFactory.Fixture import Fixture
from APS.Bucket import Bucket
from APS.Block import Block

class Machine(Resource):
    def __init__(self,Nwf):
        super(Machine, self).__init__()
        self.bucket_list = []
        # Bucket('WIP', 'random_op',  ra.randint(20000, 40000), ra.randint(40000, 60000))
        self.Nwf = Nwf
        
    def time_line_empty(self):
        if len(self.time_line)==1:
            return True
        else:
            return False
        
    def get_best_slot_info(self, rs_ES, bucket_duration):
        #回傳第一個bucket開始時間大於ES的bucket 之前的那個bucket之idx ex,[[]  |  []] return 0
        def find_position(bucket_list, ES):
            for idx, bucket in enumerate(bucket_list):
                if bucket.start>ES:
                    return idx-1
        if len(self.bucket_list)==1:
            return {'ES':max(rs_ES, self.bucket_list[-1].end), 'idx':1}
        else:
            #
            position = find_position(self.bucket_list, rs_ES)
            search_list = self.bucket_list[position:]
            done_flag = False
            for idx, bucket in enumerate(search_list[:-1]):
                next_bucket = search_list[idx+1]
                ES = max(rs_ES, bucket.end)
                space = next_bucket.start - ES
                if space >= bucket_duration:
                    return {'ES':ES, 'idx':position+idx}
            if not done_flag:
                # print('append from behind')
                return {'ES':max(rs_ES, self.bucket_list[-1].end), 'idx':len(self.bucket_list)}
   
    def reset(self):
        self.bucket_list = []
        
        
    def __str__(self):
        return "Machine_"+self.id+"("+str(self.ES)+")"  
    def __repr__(self):
        return "Machine_"+self.id+"("+str(self.ES)+")" 
    
class MachineGroup:
    def __init__(self,Nmc):
        self.id = ''
        self.mc_list = []
        self.mc_heapq = []
        self.ft_list = []
        self.generate_machine_and_fixture(Nmc)
        
    def time_line_empty(self):
        if len(self.time_line)==1:
            return True
        else:
            return False
        
    def add_bucket(self, bucket):
        if self.time_line[-1].end > bucket.start:
            diff = self.time_line[-1].end - bucket.start
            bucket.push(diff)
        bucket.start = max(self.time_line[-1].end, bucket.start)
        bucket.end = bucket.start + bucket.duration
        self.time_line.append(bucket)
        
    def generate_machine_and_fixture(self, Nmc):
        self.generate_machine(Nmc)
        self.generate_ft(Nmc)
        
    def generate_ft(self, Nmc):
        Nparallel = Nmc + ra.randint(-2, 2)
        Nft = ra.randint(2,5)
        self.ft_list = [Fixture(Nparallel) for i in range(Nft)]
        
    def generate_machine(self, Nmc):
        for j in range(Nmc):
            #治具數量
            mc = Machine(bool(ra.getrandbits(1)))
            self.mc_list.append(mc)
            hq.heappush(self.mc_heapq, mc)

    def get_earliest_available_machine(self):
        return hq.nsmallest(1,self.mc_heapq)[0]
    
    def get_Latest_available_machine(self):
        return hq.nlargest(1,self.mc_heapq)[0]
    
    def reset(self):
        pass