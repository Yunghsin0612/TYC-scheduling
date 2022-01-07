# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 13:51:41 2021

@author: DALab
"""
from VirtualFactory.Resource import Resource
import random as ra

class Fixture(Resource):
    def __init__(self, Nparallel):
        super(Fixture, self).__init__()
        self.Nparallel = Nparallel
        
    