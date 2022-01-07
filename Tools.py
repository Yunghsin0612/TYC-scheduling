# -*- coding: utf-8 -*-
"""
Title: Job Shop Scheduling Module
Version: 0.1
Author: Kuan-Chen Tseng k.c.tseng@ie.nthu.edu.tw
Copyright: Belongs to DAlab Solutions x Associates Co.,Ltd.
"""
import bisect

class Foo(object):
    def __init__(self, val):
         self.prop = val # The value to compare
    def __lt__(self, other):
         return self.prop < other.prop
    def __repr__(self):
         return 'Foo({})'.format(self.prop)

sorted_foos = sorted([Foo(7), Foo(1), Foo(3), Foo(9)])
print(bisect.bisect_left(sorted_foos, Foo(2)))
