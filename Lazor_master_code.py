import functions
from Block import Block
import numpy as np
from readFile import read_file
from itertools import combinations
import save_file

import random
import copy
import timeit


def solve(file_name):
    '''
    Thsi function takes in the lazor file name, calculates the block positions
    to solve the lazor file, and outputs the new block grid in a txt file
    '''  
    #Load lazor file variables

    Grid, fixed_Blocks, Blocks, Lazor_Path, Lazor_Dir, m, b, not_allowed, t = read_file(file_name) 
    
    #Specify how many of each block type there are
    num_reflect = Blocks[0]
    num_opaque = Blocks[1]
    num_refract = Blocks[2]
    
    num_blocks = sum(Blocks)
    
    #for each block define it as an object and store in blocks variable    
    blocks = []
    
    block_type =[]
    for i in range(1, num_reflect+1):
        block_type.append('reflect')
        
    for i in range(1, num_opaque+1):
        block_type.append('opaque')
    
    for i in range(1, num_refract+1): 
        block_type.append('refract')

    fixed_blocks_type = []
    fixed_blocks_pos = []
    for i in range(len(fixed_Blocks)):
        fixed_blocks_type.append(fixed_Blocks[i].block_type)
        fixed_blocks_pos.append(list(fixed_Blocks[i].position))
        fixed_blocks_pos[i] = [fixed_blocks_pos[i][1]+1,fixed_blocks_pos[i][0]+1]

    
    #edit not allowed to be one the same index as Blocks Allowed
    not_allowed = [[not_allowed[i][1]+1,not_allowed[i][0]+1] for i in range(len(not_allowed))]
     
    
    #create blocks allowed variable    
    blocks_allowed = [[i+1,j+1] for i in range(len(Grid)) for j in range(len(Grid[0])) if [i+1,j+1] not in not_allowed]
    
    xyblocks = []
    for i in range(len(blocks_allowed)):
        xyblocks.append([blocks_allowed[i][1],blocks_allowed[i][0]])       
    
    
    num_allowed = []
    for i in range(len(xyblocks)):
        num_allowed.append(functions.coord_to_num(Grid,xyblocks[i]))
        
    num_types = sum([1 for i in range(len(Blocks)) if Blocks[i] != 0])
    
    largeBoard = False
    
    if len(num_allowed) > 19:
        largeBoard = True
        ULC = 1
        URC = len(Grid[0])
        LRC = len(Grid[0])*len(Grid[0])
        LLC = LRC - len(Grid[0])    

    if num_types == 1:
        combos = []
        combo = list(combinations(num_allowed, len(block_type)))
        common_blocks_num = functions.valid_positions(Lazor_Path,xyblocks,Grid)
        for i in range(len(combo)):
            if any(x in common_blocks_num for x in combo[i]):
                combos.append(combo[i])
     
    
#    if num_types == 1 and largeBoard == True:
#        combos = []
#        combo = list(combinations(num_allowed, len(block_type)))
#        common_blocks_num = functions.valid_positions(Lazor_Path,xyblocks,Grid)
#        for i in range(len(combo)):
#            if any(x in common_blocks_num for x in combo[i]):
#                if ULC not in combo[i] and URC not in combo[i] and LRC not in combo[i]:
#                    combos.append(combo[i])
        
    else:
        common_blocks_num = functions.valid_positions(Lazor_Path,blocks_allowed,Grid)
        combos = functions.get_combos(block_type,num_allowed,common_blocks_num, Grid)

    print(combos)
    print(num_types)
    #define variable that checks if targets have been hit    
    target_check = np.multiply(m,t)
    
    print(len(combos))
    
    #fix things that need to be reinitialized at beginning of each while loop
    fixed_LP = copy.deepcopy(Lazor_Path)
    fixed_LD = copy.deepcopy(Lazor_Dir)
    fixed_m = copy.deepcopy(m)
    fixed_b = copy.deepcopy(b)


    branch = False
    branch_1 = None
    branch_2 = None
    branch_1_dir = None
    branch_2_dir = None
    
    total_laze = len(m)
    num = 0


    while not np.array_equal(target_check, 2*t):
        print(len(combos))
        num = num+1
        used_contact_pos = []
        blocks = []
        chosen_combo = combos[-1]
        
        for j in range(len(block_type)):
            if num_types == 1:
                b_type = block_type[0]
                b_pos = chosen_combo[j]
                b_pos = functions.num_to_coord(Grid, b_pos)
                
            else:
                b_type = chosen_combo[j]
                b_pos = chosen_combo[j+num_blocks]
                b_pos = functions.num_to_coord(Grid, b_pos)

                
            blocks.append(Block(b_type,tuple(b_pos)))    
            blocks[j].add_blocks(b)
            
        for i in range(len(fixed_Blocks)):
            blocks.append(Block(fixed_blocks_type[i],tuple(fixed_blocks_pos[i])))
            
        for i in range(len(m)):
            lazor_num = i

            contact_position, x_dir, y_dir, contact_index, contact_side, contact_list, used_contact_pos = functions.lazor_contact_tuple(m[lazor_num],b, Lazor_Path, Lazor_Dir, lazor_num, used_contact_pos, total_laze)

            while contact_position is not None:
                        
                block, b_type = functions.find_block_type(blocks, b, contact_position)
                    
                new_x_dir,new_y_dir,delete_after_contact = block.block_prop(x_dir,y_dir,contact_side)
            
                Lazor_Path, Lazor_Dir, m[lazor_num], special = functions.add_to_lazor_path(block,contact_position, m[lazor_num], Lazor_Path, Lazor_Dir, lazor_num, new_x_dir, new_y_dir, contact_index, contact_side, delete_after_contact, total_laze, used_contact_pos)

                if branch == True:
                    refract_branch, refract_branch_dir = functions.change_refract_branches(branch_1,branch_2,branch_1_dir,branch_2_dir,contact_position)
                    if refract_branch == None:
                        pass
                    else:
                        Lazor_Path[lazor_num].extend(refract_branch)
                        Lazor_Dir[lazor_num].extend(refract_branch_dir)
                        for j in range(len(refract_branch)):           
                            m[lazor_num][refract_branch[j][1]][refract_branch[j][0]] = 2
                            
                if b_type == "refract":
                    used_contact_pos.extend(contact_list)
    
                if b_type == "refract" and special == False:
                    parent,branch_1,branch_2,branch_1_dir,branch_2_dir,branch = functions.refract_branches(Lazor_Path,Lazor_Dir,lazor_num)
    
                #if special == True:
                    #used_contact_pos.pop()       
                contact_position, x_dir, y_dir, contact_index, contact_side, contact_list, used_contact_pos = functions.lazor_contact_tuple(m[lazor_num],b, Lazor_Path, Lazor_Dir, lazor_num, used_contact_pos, total_laze)


        target_check = np.multiply(sum(m),t)
        combos.remove(chosen_combo)
        Lazor_Path_sol = Lazor_Path
        b_pos_sol = b_pos
        b_type_sol = b_type
        m = copy.deepcopy(fixed_m)
        b = copy.deepcopy(fixed_b)
        branch = False
        Lazor_Path = copy.deepcopy(fixed_LP)
        Lazor_Dir = copy.deepcopy(fixed_LD)
        
    return b_pos_sol,b_type_sol,Lazor_Path_sol, Grid

        
    

if __name__ == "__main__":
    b_pos,b_type,Lazor_Path, Grid = solve('mad_1.bff')
    print(b_pos,b_type,Lazor_Path, Grid)
    save_file.save_file("solve", Grid, b_pos,b_type, Lazor_Path)