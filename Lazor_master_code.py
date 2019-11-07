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
    
        
    Lazor_Path = []
    Lazor_Dir = []      
    Lazor_Path_i = []
    Lazor_Dir_i = [] 

    #create empty matrices based on grid size
    row = len(Grid)
    col = len(Grid[0])
    m = np.zeros((2*row+1,2*col+1),dtype=int)
    b = np.zeros((2*row+1,2*col+1),dtype=int)
    
    #read fixed blocks and non permitted positions
    #fixed blocks corresponds to pos_x-1 and pos_y-1
    fixed_blocks = [[i,j] for i in range(len(Grid[0])) for j in range(len(Grid)) if Grid[j][i] == 'B']

    #adds fixed blocks to matrix
    for x in range(len(fixed_blocks)):
        b[1+((fixed_blocks[x][1])*2)][((fixed_blocks[x][0])*2)] = 1 #left
        b[((fixed_blocks[x][1])*2)][1+((fixed_blocks[x][0])*2)] =  1 #top
        b[1+((fixed_blocks[x][1])*2)][2+((fixed_blocks[x][0])*2)] = 1 #right 
        b[2+((fixed_blocks[x][1])*2)][1+((fixed_blocks[x][0])*2)] = 1

    #add possions not accessible to matrix
    not_allowed = [[i,j] for i in range(len(Grid[0])) for j in range(len(Grid)) if Grid[j][i] == 'x']

    for y in range(len(not_allowed)):
        b[1+((not_allowed[y][1])*2)][((not_allowed[y][0])*2)] = -1 #left
        b[((not_allowed[y][1])*2)][1+((not_allowed[y][0])*2)] =  -1 #top
        b[1+((not_allowed[y][1])*2)][2+((not_allowed[y][0])*2)] = -1 #right 
        b[2+((not_allowed[y][1])*2)][1+((not_allowed[y][0])*2)] = -1

    #return vector of positions x and y not allowed to place blocks
    not_allowed.extend(fixed_blocks)
    
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
        Lazor_Path_i.append([count_j[i],count_k[i]])
        Lazor_Dir_i.append([j[i],k[i]])

        while (0 <= count_k[i] < 2*row+1) and (0 <= count_j[i] < 2*col+1):
            m[count_k[i]][count_j[i]] = 2       
            count_j[i] += j[i]
            count_k[i] += k[i]
            Lazor_Path_i.append([count_j[i],count_k[i]])
            Lazor_Dir_i.append([j[i],k[i]])
       
        Lazor_Dir_i.pop()
        Lazor_Path_i.pop()    
         
        Lazor_Path.append(Lazor_Path_i)
        Lazor_Dir.append(Lazor_Dir_i)
        
        Lazor_Path_i = []
        Lazor_dir_i = []
        
    
    #Add targets to matrix m
    P = list(P)
    for i in range(len(P)):
        m[P[i][0]][P[i][1]] = 1       
            
        
    Blocks = [A, B, C]
    #print(Lazor_Path)
    return Grid, Blocks, P, Lazor_Path, Lazor_Dir, m, b, not_allowed


class block():

    def __init__(self, block_type, position):
        self.block_type = block_type
        self.position = position

    def move(self, new_position, m, b, pos_x, pos_y, lazor_path_list, lazor_dir_list):
        self.position = new_position

        for i in range(len(lazor_path_list)):
            lazor_num = i
            contact_position, x_dir, y_dir, contact_index, contact_side = self.lazor_contact_tuple(m,b,pos_x,pos_y, lazor_path_list, lazor_dir_list, lazor_num)      

        lazor_dir_list, lazor_path_list, m = self.add_to_lazor_path(contact_position, lazor_path_list, lazor_dir_list, lazor_num, x_dir, y_dir, contact_index, contact_side, m)

    def add_to_lazor_path(self, contact_position, lazor_path_list, lazor_dir_list, lazor_num, x_dir, y_dir, contact_index, contact_side, m):
        # "top" = 1
        # "bottom" = 2
        # "left" = 3
        # "right" = 4
        

        if self.block_type == "opaque":
            new_x_dir, new_y_dir = 0, 0
            delete_after_contact = True
        else:
            if contact_side == 1 or contact_side == 2:
                new_x_dir, new_y_dir = x_dir, y_dir * -1
            if contact_side == 3 or contact_side == 4:
                new_x_dir, new_y_dir = x_dir * -1, y_dir
            if self.block_type == "refract":
                delete_after_contact = False
            if self.block_type == "reflect":
                delete_after_contact = True

        Lazor_Path_i = [[contact_position[0], contact_position[1]]]
        Lazor_Dir_i = [[new_x_dir, new_y_dir]]

        r = len(m)
        l = len(m[0])

        if self.block_type != "opaque":
            while 0 <= Lazor_Path_i[-1][0] < r and 0 <= Lazor_Path_i[-1][1] < l:
                x = Lazor_Path_i[-1][0] + new_x_dir
                y = Lazor_Path_i[-1][1] + new_y_dir
                new_path = [x, y]
                new_dir = [new_x_dir, new_y_dir]
                Lazor_Path_i.append(new_path)
                Lazor_Dir_i.append(new_dir)
            Lazor_Dir_i.pop()
            Lazor_Path_i.pop()
 
        if delete_after_contact:
            del lazor_dir_list[lazor_num][contact_index+1:len(lazor_dir_list[lazor_num])+1]
            del lazor_path_list[lazor_num][contact_index+1:len(lazor_path_list[lazor_num])+1]

            if self.block_type != "opaque":
                lazor_path_list[lazor_num] = lazor_path_list[lazor_num] + Lazor_Path_i
                lazor_dir_list[lazor_num] = lazor_dir_list[lazor_num] + Lazor_Dir_i

        else:
            lazor_path_list.append(Lazor_Path_i)
            lazor_dir_list.append(Lazor_Dir_i)
        #print(lazor_dir_list)
        #print(lazor_path_list)
        
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == 2:
                    m[i][j] = 0
        
        for i in lazor_path_list[0]:
            m[i[1]][i[0]] = 2
            
            
        return lazor_dir_list, lazor_path_list, m
    
            
            


# in order to find the direction that the lazor is going when it hits the block
# we need to find the index in the lazor path list and look at that index in the lazor direction list
    def lazor_contact_tuple(self, m,b,pos_x,pos_y, lazor_path_list, lazor_dir_list, lazor_num):

        b[1+((pos_y-1)*2)][((pos_x-1)*2)] = 3  # left
        b[((pos_y-1)*2)][1+((pos_x-1)*2)] = 1  # top
        b[1+((pos_y-1)*2)][2+((pos_x-1)*2)] = 4  # right
        b[2+((pos_y-1)*2)][1+((pos_x-1)*2)] = 2  # bottom

        # element wise product to find overlapping indices of lazor and block
        # m = np.transpose(m)
        matrix_prod = np.multiply(m, b)

        if np.count_nonzero(matrix_prod) >= 1:
            contact_pos = [[i, j] for i in range(len(matrix_prod[0])) for j in range(len(matrix_prod)) if matrix_prod[j][i] >= 1]
        else:
            contact_pos = []
        
        #print(lazor_path_list[lazor_num])

        if len(contact_pos) > 0:  
            for i in lazor_path_list[lazor_num]:
                for j in contact_pos:
                    if i == j:
                        first_contact_pos = j
                        contact_index = lazor_path_list[lazor_num].index(first_contact_pos)
                        x_dir, y_dir = lazor_dir_list[lazor_num][contact_index]
                        break
                    break
        else:
            first_contact_pos = [0,0]

        print(first_contact_pos)
        #print(m)
        #print(b)

        return first_contact_pos, x_dir, y_dir, contact_index, b[first_contact_pos[1]][first_contact_pos[0]]

def load_file(file_name):
    pass



# =============================================================================
# def solve(file_name):
# 
#         #grid size = 4x4 for pilot case
#         #define blocks - refract
#         #run loop till all 1's arent 2's
#         #dot product of OG matrix and block matrix
# 
#         for k in range(3):
#             for pos_x in range(4):
#              for pos_y in range(4):
#                 pos_x = 4
#                 pos_y = 1
#                 b[1+((pos_y-1)*2)][((pos_x-1)*2)] = 1
#                 b[((pos_y-1)*2)][1+((pos_x-1)*2)] = 1  
#                 b[1+((pos_y-1)*2)][2+((pos_x-1)*2)] = 1
#                 b[2+((pos_y-1)*2)][1+((pos_x-1)*2)] = 1
# 
#         #check wether lazor hits or not
#         m = np.transpose(m)
#         print(m)
#         print(b)
#         matrix_prod = np.multiply(m,b)
#         print(matrix_prod)
# =============================================================================

if __name__ == "__main__":
    
    b1 = block("reflect", (4,1))
    Grid, Blocks, P, Lazor_Path, Lazor_Dir, m, b, not_allowed = read_file('mad_1.bff')
    
    print(m)
    print('Break')
    print(b)    
    print('New Move')
    
    
    b1.move((4, 1), m, b, 4, 1, Lazor_Path, Lazor_Dir)
    
    print(m)
    print('Break')
    print(b)
    print(Lazor_Dir)
    print(Lazor_Path)
    print('New Move')
    
    
    b2 = block("reflect", (2,1))
    b2.move((2, 3), m, b, 2, 3, Lazor_Path, Lazor_Dir)
    
    print(m)
    print('Break')
    print(b)
    print(Lazor_Dir)
    print(Lazor_Path)
    print('New Move')
    
    
# =============================================================================
#     b3 = block("refract", (3,4))
#     b3.move((3, 4), m, b, 3,4 , Lazor_Path, Lazor_Dir)
#     
#     print(m)
#     print('Break')
#     print(b)
#     print(Lazor_Dir)
#     print(Lazor_Path)
#     print('New Move')
# =============================================================================


