#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 17:52:08 2019

@author: Anusha
"""
import numpy as np
import random
from collections import Counter

class Block():
    def __init__(self, block_type, position):
        self.block_type = block_type
        self.position = position
        
    def change_position(self, new_position):
        self.position = new_position
        
        return new_position
    
    def get_type(self):
        
        return self.block_type
    
    def add_blocks(self,b):
        position = list(self.position)
        pos_x = position[0]
        pos_y = position[1]
        
        b[1+((pos_x-1)*2)][((pos_y-1)*2)] = 3 #left
        b[((pos_x-1)*2)][1+((pos_y-1)*2)] =  1 #top
        b[1+((pos_x-1)*2)][2+((pos_y-1)*2)] = 4 #right 
        b[2+((pos_x-1)*2)][1+((pos_y-1)*2)] = 2 #bottom
        
        return b
    
    def b_matrix(self):
        position = list(self.position)
        pos_x = position[0]
        pos_y = position[1]
        
        b_type = self.block_type
        #coords = [[(pos_x-1)*2,1+((pos_y-1)*2)],[1+((pos_x-1)*2),(pos_y-1)*2],[2+((pos_x-1)*2),1+((pos_y-1)*2)],[1+((pos_x-1)*2),2+((pos_y-1)*2)]]
        
        return b_type
           
    def block_prop(self,x_dir,y_dir,contact_side):
        
        if contact_side == 1 or contact_side  == 2:
            new_x_dir, new_y_dir = x_dir, y_dir*-1
        elif contact_side  == 3 or contact_side  == 4:
            new_x_dir, new_y_dir = x_dir*-1, y_dir 
        
        if self.block_type == "opaque":
            delete_after_contact = True
        else:             
            if self.block_type == "refract":
                delete_after_contact = False
            if self.block_type == "reflect":
                delete_after_contact = True
        
        return new_x_dir,new_y_dir,delete_after_contact