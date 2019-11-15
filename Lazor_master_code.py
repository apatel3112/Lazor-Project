#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Madeline Noble, Anusha Patel, Ben Toler

This file is the master code solver for the lazor game. This is the solver
that calls other files. The files that it uses are the Block, functions,
save_file, and the readFile associated with the lazor game.

"""


import functions
from Block import Block
import numpy as np
from readFile import read_file
from itertools import combinations
import save_file
import copy


def solve(file_name):
    '''
    This function takes in the lazor file name, calculates the block positions
    to solve the lazor file, and saves a file with the solution
        inputs
            file_name: name of the board file to be read
        outputs
            None
    '''
    # Load lazor file variables
    Grid, fixed_Blocks, Blocks, Lazor_Path, Lazor_Dir, m, b, not_allowed, t, P = read_file(file_name)

    # Specify how many of each block type there are
    num_reflect = Blocks[0]
    num_opaque = Blocks[1]
    num_refract = Blocks[2]
    num_blocks = sum(Blocks)

    # for each block define it as an object and store in blocks variable
    blocks = []
    block_type = []
    for i in range(1, num_reflect+1):
        block_type.append('reflect')

    for i in range(1, num_opaque+1):
        block_type.append('opaque')

    for i in range(1, num_refract+1):
        block_type.append('refract')

    fixed_blocks_type = []
    fixed_blocks_pos = []

    # for loop that organizes the fixed blocks positions and types
    for i in range(len(fixed_Blocks)):
        fixed_blocks_type.append(fixed_Blocks[i].block_type)
        fixed_blocks_pos.append(list(fixed_Blocks[i].position))
        fixed_blocks_pos[i] = [fixed_blocks_pos[i][1]+1, fixed_blocks_pos[i][0]+1]

    # not allowed are positions with a fixed block or no space
    not_allowed = [[not_allowed[i][1]+1, not_allowed[i][0]+1] for i in range(len(not_allowed))]

    # create blocks allowed variable, all spots a block is allowed
    blocks_allowed = [[i+1, j+1] for i in range(len(Grid)) for j in range(len(Grid[0])) if [i+1, j+1] not in not_allowed]

    # orientating the block positions in x, y format
    xyblocks = []
    for i in range(len(blocks_allowed)):
        xyblocks.append([blocks_allowed[i][1], blocks_allowed[i][0]])

    # converts the allowed coordinates into single numbers correlating to the
    # coordinate position
    num_allowed = []
    for i in range(len(xyblocks)):
        num_allowed.append(functions.coord_to_num(Grid, xyblocks[i]))

    # determines the number of type of blocks we have
    num_types = sum([1 for i in range(len(Blocks)) if Blocks[i] != 0])

    # determines the blocks behind and infront of the lazor
    behind, forward = functions.block_behind_lazor(Lazor_Path, Lazor_Dir, Grid)

    # checks if we only have one block type and if so cuts down on the
    # number of valid combinations for the blocks
    if num_types == 1:
        combos = []
        combo = list(combinations(num_allowed, len(block_type)))
        common_blocks_num = functions.valid_positions(Lazor_Path, xyblocks, Grid)
        i = 0
        totalBlocks = len(Grid[0])*len(Grid)
        allblocks = [i for i in range(1, totalBlocks+1)]
        avg = sum(allblocks)/len(allblocks)

        for i in range(len(combo)):
            if any(x in common_blocks_num for x in combo[i]):
                summ = 0
                k = 0
                c = list(combo[i])
                for k in range(len(block_type)):
                    summ = summ + combo[i][k]
                bavg = summ/k
                absvalue = abs(avg - bavg)
                c.append(absvalue)
                combos.append(tuple(c))

        combos = list(set(combos))

    else:
        common_blocks_num = functions.valid_positions(Lazor_Path, blocks_allowed, Grid)
        combos = functions.get_combos(block_type, num_allowed, common_blocks_num, Grid, behind, forward)

    # fix things that need to be reinitialized at beginning of each while loop
    fixed_LP = copy.deepcopy(Lazor_Path)
    fixed_LD = copy.deepcopy(Lazor_Dir)
    fixed_m = copy.deepcopy(m)
    fixed_b = copy.deepcopy(b)

    # set all of the branches for the refract block
    branch = False
    branch_1 = None
    branch_2 = None
    branch_1_dir = None
    branch_2_dir = None

    total_laze = len(m)  # total number of lazors
    num = 0
    used_contact_pos = []

    target_check = np.multiply(sum(m), t)

    # loop that will run while the correct combo is not chosen
    while not np.array_equal(target_check, 2*t):

        num = num+1
        blocks = []
        chosen_combo = combos[0]

        # place each block
        for j in range(len(block_type)):

            # if the num type is 1, we need to adjust the combo sequence
            if num_types == 1:
                b_type = block_type[0]
                b_pos = chosen_combo[j]
                b_pos = functions.num_to_coord(Grid, b_pos)

            else:
                b_type = chosen_combo[j]
                b_pos = chosen_combo[j+num_blocks]

                b_pos = functions.num_to_coord(Grid, b_pos)
            # create the blocks as objects
            blocks.append(Block(b_type, tuple(b_pos)))
            blocks[j].add_blocks(b)

        # loop through each of the lazors
        for i in range(len(m)):
            lazor_num = i
            used_contact_pos = []

            # check for blocks behind the lazor
            behind_coord = None
            if behind[i] is not None:
                behind_coord = functions.num_to_coord(Grid, behind[i])

            # determining the contact position characteristics
            contact_position, x_dir, y_dir, contact_index, contact_side, contact_list, used_contact_pos, all_contact_pos = functions.lazor_contact_tuple(m[lazor_num], b, Lazor_Path, Lazor_Dir, lazor_num, used_contact_pos, total_laze)

            # while there are still contact positions, continue to adjust the
            # lazor
            while contact_position is not None:

                # get the block and block type of the contact position
                block, b_type = functions.find_block_type(blocks, b, contact_position)
                b_pos_now = block.pos()

                # check if the block is refract, and if so update the branches
                if b_type == "refract":
                    used_contact_pos.extend(all_contact_pos)

                # check special checks if the block is at the position behind
                # where the lazor starts
                if functions.check_special(list(b_pos_now), behind_coord) is False:
                    special = False
                    new_x_dir, new_y_dir, delete_after_contact = block.block_prop(x_dir, y_dir, contact_side)
                    Lazor_Path, Lazor_Dir, m[lazor_num] = functions.add_to_lazor_path(block, contact_position, m[lazor_num], Lazor_Path, Lazor_Dir, lazor_num, new_x_dir, new_y_dir, contact_index, contact_side, delete_after_contact, total_laze, used_contact_pos, special)

                    # if a branch exists, adjust the branches accordingly
                    if branch is True:
                        refract_branch, refract_branch_dir = functions.change_refract_branches(branch_1, branch_2, branch_1_dir, branch_2_dir, contact_position)
                        if refract_branch is None:
                            pass
                        else:
                            Lazor_Path[lazor_num].extend(refract_branch)
                            Lazor_Dir[lazor_num].extend(refract_branch_dir)
                            for j in range(len(refract_branch)):
                                m[lazor_num][refract_branch[j][1]][refract_branch[j][0]] = 2

                    # if the block is refract, then create new branches
                    if b_type == "refract":
                        parent, branch_1, branch_2, branch_1_dir, branch_2_dir, branch = functions.refract_branches(Lazor_Path, Lazor_Dir, lazor_num)
                    contact_position, x_dir, y_dir, contact_index, contact_side, contact_list, used_contact_pos, all_contact_pos = functions.lazor_contact_tuple(m[lazor_num], b, Lazor_Path, Lazor_Dir, lazor_num, used_contact_pos, total_laze)

                else:
                    # if special is true, do not update the lazor path
                    special = True
                    new_x_dir, new_y_dir, delete_after_contact = block.block_prop(x_dir, y_dir, contact_side)
                    new_x_dir = x_dir
                    new_y_dir = y_dir
                    Lazor_Path, Lazor_Dir, m[lazor_num] = functions.add_to_lazor_path(block, contact_position, m[lazor_num], Lazor_Path, Lazor_Dir, lazor_num, new_x_dir, new_y_dir, contact_index, contact_side, delete_after_contact, total_laze, used_contact_pos, special)
                    if branch is True:
                        refract_branch, refract_branch_dir = functions.change_refract_branches(branch_1, branch_2, branch_1_dir, branch_2_dir, contact_position)
                        if refract_branch is None:
                            pass
                        else:
                            Lazor_Path[lazor_num].extend(refract_branch)
                            Lazor_Dir[lazor_num].extend(refract_branch_dir)
                            for j in range(len(refract_branch)):
                                m[lazor_num][refract_branch[j][1]][refract_branch[j][0]] = 2

                    if b_type == "refract":
                        parent, branch_1, branch_2, branch_1_dir, branch_2_dir, branch = functions.refract_branches(Lazor_Path, Lazor_Dir, lazor_num)

                    contact_position, x_dir, y_dir, contact_index, contact_side, contact_list, used_contact_pos, all_contact_pos = functions.lazor_contact_tuple(m[lazor_num], b, Lazor_Path, Lazor_Dir, lazor_num, used_contact_pos, total_laze)

        # reset the target check, m, b, lazor path, lazor path,
        # and remove the previously tested combo
        target_check = np.multiply(sum(m), t)
        combos.remove(chosen_combo)
        Lazor_Path_sol = Lazor_Path
        m = copy.deepcopy(fixed_m)
        b = copy.deepcopy(fixed_b)
        branch = False
        Lazor_Path = copy.deepcopy(fixed_LP)
        Lazor_Dir = copy.deepcopy(fixed_LD)

    # save the output as a png file
    save_file.save_file(file_name, Grid, blocks, Lazor_Path_sol, P)


if __name__ == "__main__":
    solve("dark_1.bff")
     solve("mad_1.bff")
     solve("mad_4.bff")
     solve("showstopper_4.bff")
     solve("numbered_6.bff")
     solve("mad_7.bff")
     solve("yarn_5.bff")
     solve("tiny_5.bff")
