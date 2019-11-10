#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 08:53:31 2019

@author: madelinenoble
"""

import functions
from Block import Block
import numpy as np
from readFile import read_file
print("here")

def solve(file_name):
    '''
    Thsi function takes in the lazor file name, calculates the block positions
    to solve the lazor file, and outputs the new block grid in a txt file
    '''  
    #Load lazor file variables
    print("here")
    Grid, fixed_Blocks, Blocks, Lazor_Path, Lazor_Dir, m, b, not_allowed, t = read_file('/Users/Anusha/Downloads/Handout_Lazor/bff_files/mad_1.bff') 
    print(Lazor_Path)
    fixed_m = m
    fixed_b = b
    
    print(fixed_b)
    
    #Specify how many of each block type there are
    num_reflect = Blocks[0]
    num_opaque = Blocks[1]
    num_refract = Blocks[2]
    
    num_blocks = sum(Blocks)
    
    #for each block define it as an object and store in blocks variable    
    blocks = []
    block_type = []
    
    block_type =[]
    for i in range(1, num_reflect+1):
        block_type.append('reflect')
        
    for i in range(1, num_opaque+1):
        block_type.append('opaque')
    
    for i in range(1, num_refract+1): 
        block_type.append('refrct')

    

    
    #edit not allowed to be one the same index as Blocks Allowed
    not_allowed = [[not_allowed[i][0]+1,not_allowed[i][1]+1] for i in range(len(not_allowed))]
    not_allowed.append([[1,4],[2,4]])
    
    #create blocks allowed variable    
    blocks_allowed = [[i+1,j+1] for i in range(len(Grid)) for j in range(len(Grid[0])) if [i+1,j+1] not in not_allowed]
    num_allowed = []
    for i in range(len(blocks_allowed)):
        num_allowed.append(functions.coord_to_num(Grid,blocks_allowed[i]))
    
    combos = get_combos(block_type,num_allowed )
    print(combos)
    print(len(combos))
    chosen_combo = random.choice(combos)
    print(chosen_combo)
    
    for i in range(num_blocks):
        b_type = chosen_combo[i]
        b_pos = chosen_combo[i+num_blocks]
        b_pos = num_to_coord(Grid, b_pos)
        print(b_type)
        print(b_pos)
        blocks.append(Block(b_type,tuple(b_pos)))
    
    print(blocks)
    
    for i in range(len(blocks)):
        blocks[i].add_blocks(b)
    
    print(b)
    

    #define variable that checks if targets have been hit    
    target_check = np.multiply(m,t)
    
    fixed_LP = Lazor_Path
    input_LP = Lazor_Path

    branch = False
    branch_1 = None
    branch_2 = None
    branch_1_dir = None
    branch_2_dir = None
    
    target_check = np.multiply(m,t)
    
    while not np.array_equal(target_check, 2*t):
        m = fixed_m
        b = fixed_b
        for i in range(len(Lazor_Path)):
            used_contact_pos = []
            lazor_num = i
            for j in range(len(blocks)):
                contact_position, x_dir, y_dir, contact_index, contact_side = functions.lazor_contact_tuple(m[i],b, Lazor_Path, Lazor_Dir, lazor_num, used_contact_pos)
                print('CP',contact_position)
                if contact_position is None:
                    break
                block, b_type = functions.find_block_type(blocks, b, contact_position)  
                
                new_x_dir,new_y_dir,delete_after_contact = block.block_prop(x_dir,y_dir,contact_side)
                
                Lazor_Path, Lazor_Dir, m[i] = functions.add_to_lazor_path(block,contact_position, m[i], Lazor_Path, Lazor_Dir, lazor_num, new_x_dir, new_y_dir, contact_index, contact_side, delete_after_contact)
                print('w',m[i])
                print('Lazor_Path',Lazor_Path)
                if branch == True:
                    refract_branch, refract_branch_dir = functions.change_refract_branches(branch_1,branch_2,branch_1_dir,branch_2_dir,contact_position)
                    Lazor_Path.extend(refract_branch)
                    Lazor_Dir.extend(refract_branch_dir)
                    for j in range(len(refract_branch)):           
                        m[lazor_num][refract_branch[j][1]][refract_branch[j][0]] = 2      
                              
                print('LP_LN',Lazor_Path)
                            
                if b_type == "refract":
                    parent,branch_1,branch_2,branch_1_dir,branch_2_dir,branch = functions.refract_branches(Lazor_Path,Lazor_Dir,lazor_num)
            
            target_check = np.multiply(m,t)

#if __name__ == "_main_":
solve('/Users/Anusha/Downloads/Handout_Lazor/bff_files/mad_1.bff')

    #Grid, Blocks, P, Lazor_Path, Lazor_Dir, m, b, not_allowed, t = read_file('/Users/Anusha/Downloads/Handout_Lazor/bff_files/mad_1.bff')

     
#    used_contact_pos = []
#    for i in range(len(Lazor_Path)):
#           lazor_num = i
#           #print('LN',lazor_num)
#           contact_position, x_dir, y_dir, contact_index, contact_side = lazor_contact_tuple(m[i],b, Lazor_Path, Lazor_Dir, lazor_num, used_contact_pos)
#                              
#           while contact_position is not None:               
#               block = find_block_type(blocks,b,contact_position) 
#               new_x_dir,new_y_dir,delete_after_contact = block.block_prop(x_dir,y_dir)
#               Lazor_Path_i, Lazor_Path, Lazor_Dir = add_to_lazor_path(block,contact_position, Lazor_Path, Lazor_Dir, lazor_num, new_x_dir, new_y_dir, contact_index, contact_side, delete_after_contact)
#               #print('LP_LN',Lazor_Path[lazor_num])
#               contact_position, x_dir, y_dir, contact_index, contact_side = lazor_contact_tuple(m[i],b, Lazor_Path, Lazor_Dir, lazor_num, used_contact_pos)

