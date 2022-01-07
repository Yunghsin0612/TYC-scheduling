# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 15:13:46 2021

@author: DALab
"""
import pandas as pd

import os,sys
# sys.path.append(os.getcwd())
# os.chdir('../VirtualFactory')
sys.path.append('VirtualFactory')
from Factory import Factory

class DataWriter:
    def __init__(self, data_len):
        self.path = '../fake_data'
        self.CURRENTTIME = pd.to_datetime('20200902090006')
        # self.rs_id_list = self.gen_route_table(self.route_id_list)
        # self.gen_ft_table(20)
    def write(self):
        fac = Factory()
        
        
# data_writer = DataWriter(30)
# data_writer.write()