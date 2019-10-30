#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:55:52 2019

@author: madelinenoble
"""


def read_file(file_name):
    Grid = []
    A= 0
    B = 0
    C = 0
    P = []
    L = []
    
    f = open(file_name, "r")
    lines = f.readlines()
    for i in range(len(lines)):
        a = lines[i].strip('\n')

        if a == "GRID START":
            b = i+1
            j = lines[b].strip('\n')
            while j != "GRID STOP":
                r = j[::2]
                Grid.append(r)
                b = b+1
                j = lines[b].strip('\n')

    for i in range(b+1, len(lines)):
        a = lines[i].strip('\n')
        try:
            if a[0] == "A":
                A = int(a[2])
            
            elif a[0] == "B":
                B = int(a[2])
            elif a[0] == "C":
                C = int(a[2])
                
            elif a[0] == "P":
                P.append((int(a[2]), int(a[4])))
                
            elif a[0] == "L":
                if a[6] == "-":
                    d3 = -1*int(a[7])
                    if a[9] == "-":
                        d4 = -1*int(a[10])
                    else:
                        d4 = int(a[9])
                else:
                    d3 = int(a[6])
                    if a[8] == "-":
                        d4 = -1*int(a[9])
                    else:
                        d4 = int(a[8])    
                
                L.append((int(a[2]), int(a[4]), d3, d4))
            
        except IndexError:
            continue
    

        
        
        
    Blocks = [A, B, C]

    return Grid, Blocks, P, L

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

