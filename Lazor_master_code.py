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

    def move(self, new_position, lazor_path):
        self.position = new_position

        new_dir = self.add_to_lazor_path("top", ((2, 3), (-1, 1)))
        return new_dir

    def add_to_lazor_path(self, contact_position, lazor_contact_tuple):
        x_dir, y_dir = lazor_contact_tuple[1]

        if self.block_type == "opaque":
            new_x_dir, new_y_dir = 0, 0

        if self.block_type == "reflect":
            if contact_position == "top" or contact_position == "bottom":
                new_x_dir, new_y_dir = x_dir, y_dir*-1
            if contact_position == "left" or contact_position == "right":
                new_x_dir, new_y_dir = x_dir*-1, y_dir

        if self.block_type == "refract":
            new_x_dir, new_y_dir = x_dir*-1, y_dir*-1

        return new_x_dir,new_y_dir


def load_file(file_name):
    pass



def solve(file_name):
    pass 

if __name__ == "__main__":
    
    b1 = block("reflect", (3,0))
    print(b1.move((2, 2), ((2, 3), (1, 1))))
    #print(ans)

