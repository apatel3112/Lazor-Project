#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 14:56:04 2019

@author: Anusha
"""

import numpy as np
import random
import readFile
from Block import Block
from itertools import combinations
from itertools import permutations
from collections import Counter

def find_block_type(blocks, b, contact_position):
    '''
        This function takes in the contact position and determines what type
        of block is being hit
        Input:
            blocks: list of all of the block objects
            b: b matrix with all of the blocks in it
            contact_position: coordinates where the lazor hits the block
        Output
            block: the block object that the lazor is hitting
            b_types[index]: the type of block that the block is
    '''
    coords = []
    b_types = []

    for i in range(len(blocks)):
        coords_i, b_type = blocks[i].b_matrix()
        b_types.append(b_type)
        coords.append(coords_i)

    index = [j for j in range(len(coords)) if contact_position in coords[j]][0]
    block = blocks[index]

    return block, b_types[index]

def check_special(contact_position, lazor_path_list, lazor_dir_list, lazor_num, new_x_dir, new_y_dir, contact_index, contact_side):
    '''
        This function checks for the special case where a block is placed
        beind a lazor start point so it touches the lazor but does not change
        the path of the lazor
        Input:
            contact_position, lazor_path_list,
            lazor_dir_list, lazor_num, new_x_dir,
            new_y_dir, contact_index, contact_side, delete_after_contact
        Output
           special; boolean: true if it is the special case and false if not
        '''
    special = False
    if contact_position == lazor_path_list[lazor_num][0]:
        if lazor_dir_list[lazor_num][0] == [1, -1] and contact_side == 4 or lazor_dir_list[lazor_num][0] == [1, -1] and contact_side == 1:
            special = True
        if lazor_dir_list[lazor_num][0] == [1, 1] and contact_side == 4 or lazor_dir_list[lazor_num][0] == [1, 1] and contact_side == 2:
            special = True
        if lazor_dir_list[lazor_num][0] == [-1, -1] and contact_side == 3 or lazor_dir_list[lazor_num][0] == [-1, -1] and contact_side == 1:
            special = True
        if lazor_dir_list[lazor_num][0] == [-1, 1] and contact_side == 3 or lazor_dir_list[lazor_num][0] == [-1, 1] and contact_side == 2:
            special = True
    return special


def add_to_lazor_path(block,contact_position, m, lazor_path_list, lazor_dir_list, lazor_num, new_x_dir, new_y_dir, contact_index, contact_side,delete_after_contact):
    '''
        This function updates the lazor and direction lists, and updates m
        Input:
            contact_position, lazor_path_list,
            lazor_dir_list, lazor_num, new_x_dir,
            new_y_dir, contact_index, contact_side, delete_after_contact
        Output
            Lazor_Path_i: list: new lazor path list
            lazor_path_list: list: updated position list
            lazor_dir_list: list: updated direction list
            m[lazor_num]: updated lazor matrix
    '''
    # checks to make sure that this is not a special case
    if check_special:
        return lazor_path_list, lazor_dir_list, m[lazor_num]

    # starts saying where the lazor hits the block
    Lazor_Path_i = [[contact_position[0], contact_position[1]]]
    Lazor_Dir_i = [[new_x_dir, new_y_dir]]

    r = len(m[lazor_num])  # height
    l = len(m[lazor_num][0])  # length

    if block.block_type != "opaque":
        while 0 <= Lazor_Path_i[-1][0] < l and 0 <= Lazor_Path_i[-1][1] < r:
            x = Lazor_Path_i[-1][0] + new_x_dir
            y = Lazor_Path_i[-1][1] + new_y_dir
            new_path = [x, y]
            new_dir = [new_x_dir, new_y_dir]
            Lazor_Path_i.append(new_path)
            Lazor_Dir_i.append(new_dir)
        Lazor_Dir_i.pop()
        Lazor_Path_i.pop()

    if delete_after_contact is True:
        if block.block_type == "opaque":
            contact_index += 1
        del lazor_dir_list[lazor_num][contact_index+1:len(lazor_dir_list[lazor_num])+1]
        del lazor_path_list[lazor_num][contact_index+1:len(lazor_path_list[lazor_num])+1]

        if block.block_type != "opaque":
            lazor_path_list[lazor_num] = lazor_path_list[lazor_num] + Lazor_Path_i
            lazor_dir_list[lazor_num] = lazor_dir_list[lazor_num] + Lazor_Dir_i
    else:
        lazor_path_list[lazor_num].extend(Lazor_Path_i)
        lazor_dir_list[lazor_num].extend(Lazor_Dir_i)

    # update matrix of 2's
    twos = [[i, j] for i in range(len(m[lazor_num][0])) for j in range(len(m[lazor_num])) if m[lazor_num][j][i] == 2]

    for i in range(len(twos)):
        m[lazor_num][twos[i][1]][twos[i][0]] = 0

    # need separate loops as len(twos) != len(lazor_path_list[lazor_num])
    for j in range(len(lazor_path_list[lazor_num])):
            m[lazor_num][lazor_path_list[lazor_num][j][1]][lazor_path_list[lazor_num][j][0]] = 2

    return Lazor_Path_i, lazor_path_list, lazor_dir_list, m[lazor_num]


def lazor_contact_tuple(m, b, lazor_path_list, lazor_dir_list, lazor_num, used_contact_pos):        

    # element wise product to find overlapping indices of lazor and block
    matrix_prod = np.multiply(m, b)

    if np.count_nonzero(matrix_prod) >= 1:
        contact_pos = [[i, j] for i in range(len(matrix_prod[0])) for j in range(len(matrix_prod)) if matrix_prod[j][i] >= 2]
    else:
        contact_pos = []

    # make sure contact_pos list doesnt already exist in used contact pos
    contact_pos = [contact_pos[i] for i in range(len(contact_pos)) if contact_pos[i] not in used_contact_pos]

    # add to used_contact_pos list to avoid repeats
    if len(contact_pos) > 0:
        index = lazor_path_list[lazor_num].index(contact_pos[0])
        x_dir, y_dir = lazor_dir_list[lazor_num][index]

        if y_dir == 1:
            rev = False
        else:
            rev = True

        first_contact_pos = sorted(contact_pos, key=lambda l: l[x_dir], reverse=rev)[0]
        used_contact_pos.extend([first_contact_pos])

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

    return first_contact_pos, x_dir, y_dir, contact_index, contact_side


def valid_positions(lazor_path, blocks_allowed):
    '''
    This function takes in the lazor path, converts it to blocks
    '''
    blockList = []

    for i in range(len(lazor_path)):
        for j in range(len(lazor_path[i])):
            if lazor_path[i][j][0] == 1:
                x = lazor_path[i][j][0]//2
                y = lazor_path[i][j][1]//2
                blockList.append([x, y]) 
            elif lazor_path[i][j][0]%2 == 0: # even
                x = lazor_path[i][j][0]//2
                y = lazor_path[i][j][1]//2
                blockList.append([x,y])
                blockList.append([x-1,y])
            else:
                x = lazor_path[i][j][0]//2
                y = lazor_path[i][j][1]//2
                blockList.append([x, y])
                blockList.append([x, y-1])

    blockList = [[blockList[i][0]+1, blockList[i][1]+1] for i in range(len(blockList))]

    lazor_blocks = [list(x) for x in set(tuple(x) for x in blockList)]
    common_blocks = [list(x) for x in set(tuple(x) for x in blockList).intersection(set(tuple(x) for x in blocks_allowed))]
    return common_blocks

def refract_branches(lazor_path_list,lazor_dir_list,lazor_num):
    # only for refract blocks - split parent lazor path into two branches and return

    a = [tuple(lazor_path_list[lazor_num][i]) for i in range(len(lazor_path_list[lazor_num]))]
    frequency = Counter(a)
    points = list(frequency.keys())
    numbers = list(frequency.values())
    contact_list = []
    contact_list = [list(points[i]) for i in range(len(numbers)) if numbers[i] == 2]
    a = [list(a[i]) for i in range(len(a))]
    for x in range(len(contact_list)):
        refract_index = [i for i in range(len(a)) if a[i] == contact_list[x]]
        parent = lazor_path_list[lazor_num][0:refract_index[0]]
        branch_1 = lazor_path_list[lazor_num][refract_index[0]:refract_index[1]]
        branch_2 = lazor_path_list[lazor_num][refract_index[1]:len(a)]
        parent_dir = lazor_dir_list[lazor_num][0:refract_index[0]]
        branch_1_dir = lazor_dir_list[lazor_num][0:refract_index[1]]
        branch_2_dir = parent_dir + lazor_dir_list[lazor_num][refract_index[1]:len(a)]
        branch = True

        return parent, branch_1, branch_2, branch_1_dir, branch_2_dir, branch


def change_refract_branches(branch_1, branch_2, branch_1_dir, branch_2_dir, contact_position):
    # keep refracted branch on Lazor Path
    if contact_position in branch_1:
        return branch_2, branch_2_dir
    elif contact_position in branch_2:
        return branch_1, branch_1_dir


def coord_to_num(Grid, coord):
    
    r = len(Grid)
    c = len(Grid[0])
    dim = r*c

    coords = [[j+1, i+1] for i in range(r) for j in range(c)]
    nums = [i+1 for i in range(dim+1)]

    index = coords.index(coord)
    return nums[index]


def num_to_coord(Grid, num):

    r = len(Grid)
    c = len(Grid[0])
    dim = r*c

    coords = [[j+1, i+1] for i in range(r) for j in range(c)]
    nums = [i+1 for i in range(dim+1)]

    index = nums.index(num)
    return coords[index]

def get_combos(Blocks, numList):
    '''
    This function takes in a list of block IDs and coordinate IDs and returns
    all of the possible combinations
    '''
    a = list(permutations(Blocks, len(Blocks)))
    b = list(combinations(numList, len(Blocks)))
    combos_with_reps = []

    for i in range(len(a)):
        for j in range(len(b)):
            combos_with_reps.append(a[i]+b[j])
    combos = list(set(combos_with_reps))

    return combos

