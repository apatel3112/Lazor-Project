#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:55:52 2019

@author: madelinenoble
"""
import numpy as np
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
                
                L.append([int(a[2]), int(a[4]), d3, d4])
            
        except IndexError:
            continue
    

        
        
        
    Blocks = [A, B, C]

    return Grid, Blocks, P, L



class block():
    "top" = 1
    "bottom" = 2
    "left" = 3
    "right" = 4
    def __init__(self, block_type, position):
        self.block_type = block_type
        self.position = position

    def move(self, new_position, m, b, pos_x, pos_y):
        self.position = new_position
        self.lazor_contact_tuple(m,b,pos_x,pos_y)

        new_dir = self.add_to_lazor_path("top", ((2, 3), (-1, 1)))
        return new_dir

    def add_to_lazor_path(self, contact_position, lazor_contact_tuple):
        x_dir, y_dir = lazor_contact_tuple[1]

        if self.block_type == "opaque":
            new_x_dir, new_y_dir = 0, 0
            delete_after_contact = True

        elif: 
            if contact_position == "top" or contact_position == "bottom":
                new_x_dir, new_y_dir = x_dir, y_dir*-1
            if contact_position == "left" or contact_position == "right":
                new_x_dir, new_y_dir = x_dir*-1, y_dir 
            if self.block_type == "refract":
                delete_after_contact = False
            if self.block_type == "reflect":
                delete_after_contact = True

        return new_x_dir,new_y_dir , delete_after_contact

    def lazor_contact_tuple(self, m,b,pos_x,pos_y,x_dir,y_dir):
        b[1+((pos_y-1)*2)][((pos_x-1)*2)] = 3 #left
        b[((pos_y-1)*2)][1+((pos_x-1)*2)] =  1 #top
        b[1+((pos_y-1)*2)][2+((pos_x-1)*2)] = 4 #right 
        b[2+((pos_y-1)*2)][1+((pos_x-1)*2)] = 2 #bottom

        #element wise product to find overlapping indices of lazor and block
        m = np.transpose(m)
        matrix_prod = np.multiply(m,b)
        
     
        contact_pos = [[j,i] for j in len(matrix_prod[0]) for i in len(matrix_prod) if matrix_prod[j][i] >= 1]
        
        if len(contact_pos) > 1:
            #determine first contact position
            

def load_file(file_name):
    pass



def solve(file_name):
    
        m = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0]]
        m = np.array(m)
        
        #set lazors and targets
        #switch i and j indices and then transpose to get accurate result
        m[7][2] = 2
        m[3][0] = 1
        m[4][3] = 1
        m[2][5] = 1
        m[4][7] = 1
        
        targets = [[3,0],[4,3],[2,5],[4,7]]
        
        #direction of lazor
        [i,j] = [1,-1]
        count_i = 2
        count_j = 7
        lazor_path = []
        
        #lazor path on matrix
        while max(count_i,count_j) != 9:
            m[count_i][count_j] = 2       
            count_i += i
            count_j += j
            lazor_path.append([i,j])
            
        #create identical empty block matrix
        b = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0]]
        b = np.array(b)
        
        
        #grid size = 4x4 for pilot case
        #define blocks - refract
        #run loop till all 1's arent 2's
        #dot product of OG matrix and block matrix
        
        for k in range(3):
            for pos_x in range(4):
             for pos_y in range(4):
                pos_x = 4
                pos_y = 1
                b[1+((pos_y-1)*2)][((pos_x-1)*2)] = 1
                b[((pos_y-1)*2)][1+((pos_x-1)*2)] = 1  
                b[1+((pos_y-1)*2)][2+((pos_x-1)*2)] = 1
                b[2+((pos_y-1)*2)][1+((pos_x-1)*2)] = 1
        
        #check wether lazor hits or not
        m = np.transpose(m)
        print(m)
        print(b)
        matrix_prod = np.multiply(m,b)
        print(matrix_prod)

if __name__ == "__main__":
    
    b1 = block("reflect", (3,0))
    print(b1.move((2, 2), ((2, 3), (1, 1))))
    print(ans)
    
    Grid, Block, Targets, Lazors = read_file('yarn_5.bff')

