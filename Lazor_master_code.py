#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:55:52 2019

@author: madelinenoble
"""

class block():
 
    def __init__(self, block_type, position):
        self.block_type = block_type
        self.position = position
# takes in the point on the block that it is hit at
# return were the lazor goes (what are all teh coordinates that it passes throug) 
# after each one
        
    def move(self, new_position, lazor_path):
        self.position = new_position
        lazor_path_new(new_position, lazor_path):
    
    def get_location(self):
        return self.position
    
    def get_type(self):
        return self.block_type


    def new_path(self,new_position, old_path):
        if self.block == "opaque":
            
        if self.block = "reflect":
            pass
        if self.block == "refract":
            pass

def load_file(file_name):
    pass




def solve(file_name):
    
    b1 = block("opaque")
    b2 = block("reflect")
    b3 = block("refract")
    lazor_path = new_path(b1, (2,3), lazor_path)
    b1.move(2,3)
    pass

