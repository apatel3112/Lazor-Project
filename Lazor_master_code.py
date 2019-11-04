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
                r = j.replace(" ", "")
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
                P.append([int(a[2]), int(a[4])])
                
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
    
        
    r = len(Grid[0])*2 + 1
    l = len(Grid)*2 + 1
    
    Lazor_Path = []
    Lazor_Dir = []
    
    for i in range(len(L)):
        
        Lazor_Path_i = [(L[i][0], L[i][1])]
        Lazor_Dir_i = [(L[i][2], L[i][3])]  
    
        while 0 <= Lazor_Path_i[-1][0] <= r and 0 <= Lazor_Path_i[-1][1] <= l:
            x = Lazor_Path_i[-1][0] + L[i][2]
            y = Lazor_Path_i[-1][1] + L[i][3]
            new_path = (x,y)
            new_dir = (L[i][2], L[i][3])
            Lazor_Path_i.append(new_path)
            Lazor_Dir_i.append(new_dir)

        Lazor_Path_i.pop()
        Lazor_Dir_i.pop()
        Lazor_Path.append(Lazor_Path_i)
        Lazor_Dir.append(Lazor_Dir_i)
        
    #create empty matrices based on grid size
    row = len(Grid)
    col = len(Grid[0])
    m = np.zeros((2*row+1,2*col+1),dtype=int)
    b = np.zeros((2*row+1,2*col+1),dtype=int)
    
    #create vectors for x and y directions if more than 1 Lazor
    j = []
    k = []
    count_j = []
    count_k = []
    
    #lazor direction
    for i in range(len(L)):
        j.append(L[i][2])
        k.append(L[i][3])
        count_j.append(L[i][0])
        count_k.append(L[i][1])
    
          
    #determine smaller dimension if asymmetric matrix
    matrix_dim = [row,col]
    min_index = matrix_dim.index(min(matrix_dim))
    if min_index == 0:
        min_pos = count_k
    else:
        min_pos = count_j
    
    #Add lazor path on matrix m
    for i in range(len(L)):
    
        while -1 < min_pos[i] < (2*matrix_dim[min_index]+1):
            m[count_k[i]][count_j[i]] = 2       
            count_j[i] += j[i]
            count_k[i] += k[i]
        
    
    #Add targets to matrix m
    P = list(P)
    for i in range(len(P)):
        m[P[i][0]][P[i][1]] = 1       
            
        
    Blocks = [A, B, C]

    return Grid, Blocks, P, Lazor_Path, Lazor_Dir, m, b
        



class block():
    
    def __init__(self, block_type, position):
        self.block_type = block_type
        self.position = position


    def move(self, new_position, m, b, pos_x, pos_y, lazor_path_list, lazor_dir_list):
        self.position = new_position

        for i in range(len(lazor_path_list)):
            lazor_num = i
            contact_position, x_dir, y_dir, contact_index, contact_side = self.lazor_contact_tuple(m,b,pos_x,pos_y, lazor_path_list, lazor_dir_list, lazor_num)      

        self.add_to_lazor_path(contact_position, lazor_path_list, lazor_dir_list, lazor_num, x_dir, y_dir, contact_index, contact_side)

    def add_to_lazor_path(self, contact_position, lazor_path_list, lazor_dir_list, lazor_num, x_dir, y_dir, contact_index, contact_side):
        # "top" = 1
        # "bottom" = 2
        # "left" = 3
        # "right" = 4

        if self.block_type == "opaque":
            new_x_dir, new_y_dir = 0, 0
            delete_after_contact = True
        else: 
            if contact_side == 1 or contact_side  == 2:
                new_x_dir, new_y_dir = x_dir, y_dir*-1
            if contact_side  == 3 or contact_side  == 4:
                new_x_dir, new_y_dir = x_dir*-1, y_dir 
            if self.block_type == "refract":
                delete_after_contact = False
            if self.block_type == "reflect":
                delete_after_contact = True
        
             
        if delete_after_contact:
            del lazor_dir_list[lazor_num][contact_index+1:len(lazor_dir_list[lazor_num])+1]
            del lazor_path_list[lazor_num][contact_index+1:len(lazor_path_list[lazor_num])+1]
            # we should probably have another functiont that produces the rest of the lists

            
            Lazor_Path_i = [(contact_position[0], contact_position[1])]
            Lazor_Dir_i =  [(new_x_dir, new_y_dir)]

            r = 9
            l = 9

            while 0 <= Lazor_Path_i[-1][0] <= r and 0 <= Lazor_Path_i[-1][1] <= l:
                x = Lazor_Path_i[-1][0] + new_x_dir
                y = Lazor_Path_i[-1][1] + new_y_dir
                new_path = (x,y)
                new_dir = (new_x_dir, new_y_dir)
                Lazor_Path_i.append(new_path)
                Lazor_Dir_i.append(new_dir)
 
                
            Lazor_Dir_i.pop()
            Lazor_Path_i.pop()
            
            
            lazor_path_list.append(Lazor_Path_i)
            lazor_dir_list.append(Lazor_Dir_i)
            print(lazor_path_list)
            print(lazor_dir_list)
        
       # else:
            # we just add a new row for the existing lazorr
        #    lazor_dir_list.append()
         #   lazor_path_list.append()

        return lazor_dir_list, lazor_path_list
    

# in order to find the direction that the lazor is going when it hits the block
# we need to find the index in the lazor path list and look at that index in the lazor direction list
    def lazor_contact_tuple(self, m,b,pos_x,pos_y, lazor_path_list, lazor_dir_list, lazor_num):

        b[1+((pos_y-1)*2)][((pos_x-1)*2)] = 3 #left
        b[((pos_y-1)*2)][1+((pos_x-1)*2)] =  1 #top
        b[1+((pos_y-1)*2)][2+((pos_x-1)*2)] = 4 #right 
        b[2+((pos_y-1)*2)][1+((pos_x-1)*2)] = 2 #bottom

        #element wise product to find overlapping indices of lazor and block
        m = np.transpose(m)
        matrix_prod = np.multiply(m,b)
        
        if np.count_nonzero(matrix_prod) >= 1:
            contact_pos = [[j,i] for j in range(len(matrix_prod[0])) for i in range(len(matrix_prod)) if matrix_prod[j][i] >= 1]
        else:
            contact_pos = []
        
        i = 0
        x_dir, y_dir = lazor_dir_list[lazor_num][i]
        if x_dir == 1:            
            rev = False
        else:
            rev = True
        first_contact_pos = sorted(contact_pos, key=lambda l:l[y_dir], reverse=rev)[0]
        
        while lazor_path_list[lazor_num][i] != first_contact_pos:
            contact_index = i
            i += 1
        
        return first_contact_pos, x_dir, y_dir, contact_index, b[first_contact_pos[0]][first_contact_pos[1]]
   
def load_file(file_name):
    pass



def solve(file_name):
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

