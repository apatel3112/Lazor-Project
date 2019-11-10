#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:55:52 2019

@author: madelinenoble
"""
import numpy as np
import random


from collections import Counter


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
    Grid = [b.replace('B', 'A') for b in Grid]
    print(Grid)
    
    m = []
    for i in range(len(L)):
        c = np.zeros((2*row+1,2*col+1),dtype=int)
        m.append(c)
   
    b = np.zeros((2*row+1,2*col+1),dtype=int)
    t = np.zeros((2*row+1,2*col+1),dtype=int)
    
    #read fixed blocks and non permitted positions
    #fixed blocks corresponds to pos_x-1 and pos_y-1
    fixed_blocks = [[i,j] for i in range(len(Grid[0])) for j in range(len(Grid)) if Grid[j][i] == 'B' or Grid[j][i] == 'A' or Grid[j][i] == 'C']
    fixed_Blocks = []
    
    for i in range(len(fixed_blocks)):
        if Grid[fixed_blocks[i][1]][fixed_blocks[i][0]] == 'B':
            i = block("opaque", (0,0))
            fixed_Blocks.append(i)
        elif Grid[fixed_blocks[i][1]][fixed_blocks[i][0]] == 'A':
            i = block("reflect", (0,0))
            fixed_Blocks.append(i)
        elif Grid[fixed_blocks[i][1]][fixed_blocks[i][0]] == 'C':
            i = block("reflect", (0,0))
            fixed_Blocks.append(i)
            
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
    
    Lazor_Path = []
    Lazor_Dir = []      
    Lazor_Path_i = []
    Lazor_Dir_i = [] 

    #create empty matrices based on grid size
    row = len(Grid)
    col = len(Grid[0])
    
    m = []
    for i in range(len(L)):
        c = np.zeros((2*row+1,2*col+1),dtype=int)
        m.append(c)
   
    b = np.zeros((2*row+1,2*col+1),dtype=int)
    t = np.zeros((2*row+1,2*col+1),dtype=int)
    
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

    #Add lazor path on matrix m
    for i in range(len(L)):
        Lazor_Path_i.append([count_j[i],count_k[i]])
        Lazor_Dir_i.append([j[i],k[i]])

        while 0 <= count_k[i] < 2*row+1 and 0 <= count_j[i] < 2*col+1:
            m[i][count_k[i]][count_j[i]] = 2       
            count_j[i] += j[i]
            count_k[i] += k[i]
            Lazor_Path_i.append([count_j[i],count_k[i]])
            Lazor_Dir_i.append([j[i],k[i]])
       
        Lazor_Dir_i.pop()
        Lazor_Path_i.pop()    
         
        Lazor_Path.append(Lazor_Path_i)
        Lazor_Dir.append(Lazor_Dir_i)
        
        Lazor_Path_i = []
        Lazor_Dir_i = []
        
    
    #Add targets to matrix m
    P = list(P)
    for i in range(len(P)):
        t[P[i][1]][P[i][0]] = 1       
            
        
    Blocks = [A, B, C]

    return Grid, Blocks, P, Lazor_Path, Lazor_Dir, m, b, not_allowed, t
        


used_contact_pos = []

class block():

    def __init__(self, block_type, position):
        self.block_type = block_type
        self.position = position

    def move(self, new_position, m, b, pos_x, pos_y, lazor_path_list, lazor_dir_list):
        self.position = new_position


        for i in range(len(lazor_path_list)):
            lazor_num = i
            contact_position, x_dir, y_dir, contact_index, contact_side = self.lazor_contact_tuple(m[i],b,pos_x,pos_y, lazor_path_list, lazor_dir_list, lazor_num, used_contact_pos)      
            if contact_position is not None:
                Lazor_Path_i, lazor_path_list, lazor_dir_list = self.add_to_lazor_path(contact_position, lazor_path_list, lazor_dir_list, lazor_num, x_dir, y_dir, contact_index, contact_side)
        return Lazor_Path_i
    
    #def contact_points(self, lazor_path_list):
        
      
        #return contact_list,refract_index
                
    def add_to_lazor_path(self,contact_position, lazor_path_list, lazor_dir_list, lazor_num, x_dir, y_dir, contact_index, contact_side):
        # "top" = 1
        # "bottom" = 2
        # "left" = 3
        # "right" = 4
        if contact_side == 1 or contact_side  == 2:
            new_x_dir, new_y_dir = x_dir, y_dir*-1
        elif contact_side  == 3 or contact_side  == 4:
            new_x_dir, new_y_dir = x_dir*-1, y_dir 
                
        if self.block_type == "opaque":
            new_x_dir, new_y_dir = 0, 0
            delete_after_contact = True
        else:             
            if self.block_type == "refract":
                delete_after_contact = False
            if self.block_type == "reflect":
                delete_after_contact = True

        Lazor_Path_i = [[contact_position[0], contact_position[1]]]
        Lazor_Dir_i =  [[new_x_dir, new_y_dir]]
        
        print('LDI',Lazor_Dir_i)
        print(self.block_type)
        print(self.position)
        
        r = len(m[lazor_num])
        l = len(m[lazor_num][0])

        if self.block_type != "opaque":
            while 0 <= Lazor_Path_i[-1][0] < l and 0 <= Lazor_Path_i[-1][1] < r:
                x = Lazor_Path_i[-1][0] + new_x_dir
                y = Lazor_Path_i[-1][1] + new_y_dir
                new_path = [x,y]
                new_dir = [new_x_dir, new_y_dir]
                Lazor_Path_i.append(new_path)
                Lazor_Dir_i.append(new_dir)
            Lazor_Dir_i.pop()
            Lazor_Path_i.pop()
        
        
        if delete_after_contact is True:
            if self.block_type == "opaque":
                contact_index += 1
                
            del lazor_dir_list[lazor_num][contact_index+1:len(lazor_dir_list[lazor_num])+1]
            del lazor_path_list[lazor_num][contact_index+1:len(lazor_path_list[lazor_num])+1]
            
            if self.block_type != "opaque":
                lazor_path_list[lazor_num] = lazor_path_list[lazor_num] + Lazor_Path_i
                lazor_dir_list[lazor_num] = lazor_dir_list[lazor_num] + Lazor_Dir_i
        else:
               lazor_path_list[lazor_num].extend(Lazor_Path_i)
               lazor_dir_list[lazor_num].extend(Lazor_Dir_i)
               
        print('LPL',lazor_path_list[lazor_num])
        
        #only for refract blocks
#        if self.block_type == "refract":
#            a = [tuple(lazor_path_list[lazor_num][i]) for i in range(len(lazor_path_list[lazor_num]))]
#            frequency = Counter(a)
#            points = list(frequency.keys())
#            numbers = list(frequency.values())
#            contact_list = []    
#            contact_list = [list(points[i]) for i in range(len(numbers)) if numbers[i] == 2]    
#            a = [list(a[i]) for i in range(len(a))]
#            for x in range(len(contact_list)):
#                refract_index = [i for i in range(len(a)) if a[i] == contact_list[x]]
#                parent = lazor_path_list[lazor_num][0:refract_index[0]]
#                branch_1 = lazor_path_list[lazor_num][0:refract_index[1]]
#                branch_2 = parent + lazor_path_list[lazor_num][refract_index[1]:len(a)]
#                parent_dir = lazor_dir_list[lazor_num][0:refract_index[0]]
#                branch_1_dir = lazor_dir_list[lazor_num][0:refract_index[1]]
#                branch_2_dir = parent_dir + lazor_dir_list[lazor_num][refract_index[1]:len(a)]

        #update matrix of 2's        
        twos = [[i,j] for i in range(len(m[lazor_num][0])) for j in range(len(m[lazor_num])) if m[lazor_num][j][i] == 2]

        
        for i in range(len(twos)):
            m[lazor_num][twos[i][1]][twos[i][0]] = 0

        #need separate loops as len(twos) != len(lazor_path_list[lazor_num])
        for j in range(len(lazor_path_list[lazor_num])):           
                m[lazor_num][lazor_path_list[lazor_num][j][1]][lazor_path_list[lazor_num][j][0]] = 2
        
        print(m)
        print(lazor_num)
        return Lazor_Path_i, lazor_dir_list, lazor_path_list #branch_1, branch_2, branch_1_dir, branch_2_dir
        


# in order to find the direction that the lazor is going when it hits the block
# we need to find the index in the lazor path list and look at that index in the lazor direction list
    def lazor_contact_tuple(self, m,b,pos_x,pos_y, lazor_path_list, lazor_dir_list, lazor_num, used_contact_pos):

        b[1+((pos_y-1)*2)][((pos_x-1)*2)] = 3 #left
        b[((pos_y-1)*2)][1+((pos_x-1)*2)] =  1 #top
        b[1+((pos_y-1)*2)][2+((pos_x-1)*2)] = 4 #right 
        b[2+((pos_y-1)*2)][1+((pos_x-1)*2)] = 2 #bottom

        #element wise product to find overlapping indices of lazor and block
        # m = np.transpose(m)
        matrix_prod = np.multiply(m,b)
       
        if np.count_nonzero(matrix_prod) >= 1:
            contact_pos = [[i,j] for i in range(len(matrix_prod[0])) for j in range(len(matrix_prod)) if matrix_prod[j][i] >= 2]
        else:
            contact_pos = []
        

        #make sure contact_pos list doesnt already exist in used contact pos
        contact_pos = [contact_pos[i] for i in range(len(contact_pos)) if contact_pos[i] not in used_contact_pos]
        


        #add to used_contact_pos list to avoid repeats
        if len(contact_pos) > 0:
            index = lazor_path_list[lazor_num].index(contact_pos[0])           
            x_dir, y_dir = lazor_dir_list[lazor_num][index]
            
            if y_dir == 1:      
                rev = False
            else:
                rev = True
            
            first_contact_pos = sorted(contact_pos, key=lambda l:l[x_dir], reverse=rev)[0]
            used_contact_pos.extend(contact_pos)

            
            contact_index = 0
            i = 0
            while lazor_path_list[lazor_num][i] != first_contact_pos:
                contact_index = i
                i += 1
            contact_side = b[first_contact_pos[1]][first_contact_pos[0]]
        else:
            first_contact_pos = None
            contact_index = None
            contact_side = None
            x_dir = None
            y_dir = None
            
        print('FCP',first_contact_pos)
        return first_contact_pos, x_dir, y_dir, contact_index,contact_side
 
def valid_positions(lazor_path, Blocks_Allowed):
    '''
    This function takes in the lazor path, converts it to blocks
    '''
    blockList = []
    for i in range(len(lazor_path)):
        for j in range(len(lazor_path[i])):
            if lazor_path[i][j][0]%2 == 0: # even
                x = lazor_path[i][j][0]//2
                y = lazor_path[i][j][1]//2
                blockList.append([x,y])
                blockList.append([x-1,y])
            else:
                x = lazor_path[i][j][0]//2
                y = lazor_path[i][j][1]//2
                blockList.append([x,y])
                blockList.append([x,y-1])
    
    blockList = [[blockList[i][0]+1,blockList[i][1]+1] for i in range(len(blockList))]
    #print(blockList)
    
    #print(common_blocks)
    lazor_blocks = [list(x) for x in set(tuple(x) for x in blockList)]
    common_blocks = [list(x) for x in set(tuple(x) for x in blockList).intersection(set(tuple(x) for x in Blocks_Allowed))]
    print("common", common_blocks)
    return common_blocks


def save_file(file_name, solved_grid):
    '''
    This function weites the solved grids from file_name on to a new txt file
    '''
    
    #specidy solved file name from old file name
    new_file_name = "%s_%s" % ("solved", file_name)
    
    #open new file under as new_file_name and assign it to variable new_file
    new_file = open(new_file_name, "w+")
    
    
    #write each element of solved grid onto a new line in the new fiel
    for line in solved_grid:
        new_file.write("%s/n" % line)
        
        
    #close the new file    
    new_file.close()
    
    
    

def solve(file_name):
    '''
    Thsi function takes in the lazor file name, calculates the block positions
    to solve the lazor file, and outputs the new block grid in a txt file
    '''
    
    #Load lazor file variables
    Grid, Blocks, P, Lazor_Path, Lazor_Dir, m, b, not_allowed, t = read_file(file_name)
    
    fixed_m = m
    
    #Specify how many of each block type there are
    num_reflect = Blocks[0]
    num_opaque = Blocks[1]
    num_refract = Blocks[2]
    
    
    #for each block define it as an object and store in blocks variable
    blocks = []
    block_type =[]
    for i in range(1, num_reflect+1):
        i = block("reflect", (0,0))
        blocks.append(i)
        block_type.append('A')
        
    for i in range(1, num_opaque+1):
        i = block("opaque", (0,0))
        blocks.append(i)
        block_type.append('B')
    
    for i in range(1, num_refract+1):
        i = block("refract", (0,0))
        blocks.append(i)
        block_type.append('C')
    
    #edit not allowed to be one the same index as Blocks Allowed
    for i in range(len(not_allowed)):
        for j in range(len(not_allowed[0])):
            new = not_allowed[i][j] + 1
            not_allowed[i][j] = new
    
    #create blocks allowed variable    
    Blocks_Allowed = []
    for i in range(len(Grid)):
        for j in range(len(Grid[0])):
            Blocks_Allowed.append([i+1,j+1])
                       
    #edit blocks allowed to exlcude not_allowed blocks
    for i in not_allowed:
        Blocks_Allowed.remove(i)

    print(Blocks_Allowed)
            
    #define variable that checks if targets have been hit    
    target_check = np.multiply(m,t)
    
    #if position_check is the same as two times the position matrix loop breaks
    while not np.array_equal(target_check, 2*t):  
        #create blocks allowed variable    
        Blocks_Allowed = []
        for i in range(len(Grid)):
            for j in range(len(Grid[0])):
                Blocks_Allowed.append([i+1,j+1])
                           
        #edit blocks allowed to exlcude not_allowed blocks
        for i in not_allowed:
            Blocks_Allowed.remove(i)

        #for each block object, randomly choose a position in the grid
        lazor_path_i = Lazor_Path
        block_pos = []
        for i in range(len(blocks)):
            valid_pos = valid_positions(lazor_path_i, Blocks_Allowed)
            pos = random.choice(valid_pos)
            lazor_path_i = blocks[i].move((pos[0], pos[1]), m, b, pos[0], pos[1], Lazor_Path, Lazor_Dir)
            block_pos.append(pos)
            Blocks_Allowed.remove(pos)           
            m = fixed_m
        
        #with all blokcs position re-calculate the postion check
        target_check = np.multiply(m,t)
    
    
    solved_grid = Grid    
    for i in len(block_pos):
        solved_grid[block_pos[i][0]-1][block_pos[i][1]-1] = block_type[i]
        
            
    save_file(file_name, solved_grid)
    

if __name__ == "__main__":
    solve('mad_1.bff')
#    b1 = block("refract", (4,1))
#    Grid, Blocks, P, Lazor_Path, Lazor_Dir, m, b, not_allowed, t = read_file('mad_1.bff')
#    b1.move((4, 1), m, b, 4, 1, Lazor_Path, Lazor_Dir)
#    b2 = block("reflect", (2,3))
#    b2.move((2, 3), m, b, 2, 3, Lazor_Path, Lazor_Dir)
#
#    print(Lazor_Path)
#    print(Lazor_Dir)

        
