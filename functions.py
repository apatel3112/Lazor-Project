#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
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
    # check for the index position of the coordinate where we have contact
    try:
        index = [j for j in range(len(coords)) if contact_position in coords[j]][0]
        block = blocks[index]
    # if an index error is thrown then the index is 1
    except IndexError:
        index = 1
        block = blocks[index]

    return block, b_types[index]


def check_special(b_pos, behind):
    '''
        This function checks for the special case where a block is placed
        beind a lazor start point so it touches the lazor but does not change
        the path of the lazor
        Input:
            b_pos: tupel: position of the block
            behind: the position behind where the lazor starts
        Output
           boolean: true if the special case is true, false if not
        '''

    if behind is None:
        return False
    elif b_pos == behind:
        return True
    else:
        return False


def add_to_lazor_path(block, contact_position, m, lazor_path_list, lazor_dir_list, lazor_num, new_x_dir, new_y_dir, contact_index, contact_side, delete_after_contact, total_laze, used_contact_pos, special):
    '''
        This function updates the lazor and direction lists, and updates m
        Input:
            There are many input variables, they are listed below.
            contact_position, lazor_path_list,
            lazor_dir_list, lazor_num, new_x_dir,
            new_y_dir, contact_index, contact_side, delete_after_contact
        Output
            Lazor_Path_i: list: new lazor path list
            lazor_path_list: list: updated position list
            lazor_dir_list: list: updated direction list
            m[lazor_num]: updated lazor matrix
    '''

    # starts saying where the lazor hits the block
    Lazor_Path_i = [[contact_position[0], contact_position[1]]]
    Lazor_Dir_i = [[new_x_dir, new_y_dir]]

    r = len(m)  # height
    l = len(m[0])  # length

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

    # deletes the lazor path after contact if the block is reflect and it is
    # not a special case
    if delete_after_contact is True:
        if block.block_type == "opaque" and special is False:
            contact_index += 1
            del lazor_dir_list[lazor_num][contact_index+1:len(lazor_dir_list[lazor_num])+1]
            del lazor_path_list[lazor_num][contact_index+1:len(lazor_path_list[lazor_num])+1]

        if block.block_type == "opaque" and special is True:
            lazor_path_list[lazor_num] = lazor_path_list[lazor_num] + Lazor_Path_i
            lazor_dir_list[lazor_num] = lazor_dir_list[lazor_num] + Lazor_Dir_i

        if block.block_type != "opaque":
            del lazor_dir_list[lazor_num][contact_index+1:len(lazor_dir_list[lazor_num])+1]
            del lazor_path_list[lazor_num][contact_index+1:len(lazor_path_list[lazor_num])+1]
            lazor_path_list[lazor_num] = lazor_path_list[lazor_num] + Lazor_Path_i
            lazor_dir_list[lazor_num] = lazor_dir_list[lazor_num] + Lazor_Dir_i
    else:
        lazor_path_list[lazor_num] = lazor_path_list[lazor_num] + Lazor_Path_i
        lazor_dir_list[lazor_num] = lazor_dir_list[lazor_num] + Lazor_Dir_i

    # update matrix of 2's
    twos = [[i, j] for i in range(len(m[0])) for j in range(len(m)) if m[j][i] == 2]

    for i in range(len(twos)):
        m[twos[i][1]][twos[i][0]] = 0

    # need separate loops as len(twos) != len(lazor_path_list[lazor_num])
    for j in range(len(lazor_path_list[lazor_num])):
        m[lazor_path_list[lazor_num][j][1]][lazor_path_list[lazor_num][j][0]] = 2

    return lazor_path_list, lazor_dir_list, m


def lazor_contact_tuple(m, b, lazor_path_list, lazor_dir_list, lazor_num, used_contact_pos, total_laze):
    '''
        This function takes in m and b and returns the attributes of the
        contact position
        Input:
            There are many input variables, they are listed below.
            m, b, lazor_path_list, lazor_dir_list, lazor_num, used_contact_pos,
            total_laze
        Output
            first_contact_pos: tuple, the first contact position the lazor hits
            x_dir: int, the x direction of teh lazor when it hits the position
            y_dir: int, y direction of the lazor
            contact_index: int, index in the contact list where the contact position is
            contact_side: int, representes side of the block contacted
            contact_pos: list of all contact positions
            used_contact_pos: list of previous used contact positions
            all_contact_pos: all contact positions ever hit
    '''

    # element wise product to find overlapping indices of lazor and block
    matrix_prod = np.multiply(m, b)
    if np.count_nonzero(matrix_prod) >= 1:
        contact_pos = [[i, j] for i in range(len(matrix_prod[0])) for j in range(len(matrix_prod)) if matrix_prod[j][i] >= 2]
    else:
        contact_pos = []

    # make sure contact_pos list doesnt already exist in used contact pos
    contact_pos = [contact_pos[i] for i in range(len(contact_pos)) if contact_pos[i] not in used_contact_pos]

    # add to used_contact_pos list to avoid repeats
    all_contact_pos = contact_pos

    # if there are multiple contact positions, find the first one
    if len(contact_pos) > 0:
        try:
            index = lazor_path_list[lazor_num].index(contact_pos[0])
            x_dir, y_dir = lazor_dir_list[lazor_num][index]

        except ValueError:
            index = lazor_path_list.index(contact_pos[0])
            x_dir, y_dir = lazor_dir_list[index]

        # y direction tells us how to sort our contact position list
        if y_dir == 1:
            rev = False
        else:
            rev = True

        first_contact_pos = sorted(contact_pos, key=lambda l: l[x_dir], reverse=rev)[0]

        # remember which contact positions we have used
        used_contact_pos.extend([first_contact_pos])

        contact_index = 0
        i = 0
        # get index of contact position in lazor path
        try:
            index = lazor_path_list[lazor_num].index(first_contact_pos)
            while lazor_path_list[lazor_num][i] != first_contact_pos:
                contact_index = i
                i += 1

        except ValueError:
            while lazor_path_list[i] != first_contact_pos:
                contact_index = i
                i += 1

        contact_side = b[first_contact_pos[1]][first_contact_pos[0]]

    else:
        first_contact_pos = None
        contact_index = None
        contact_side = None
        x_dir = None
        y_dir = None

    return first_contact_pos, x_dir, y_dir, contact_index, contact_side, contact_pos, used_contact_pos, all_contact_pos


def valid_positions(lazor_path, blocks_allowed, Grid):
    '''
    This function takes in the lazor path, and determines the coordinates of
    the allowed blocks that it goes through
        inputs
            lazor_path: nested list, path of the lazor
            blocks_allowed: nested list, coordinates of spaces where we can
            place blocks
            Grid: list, list of the grid from the read file
        outputs
            common_blocks_num: list of number coorelating to the coordinates
            that we can place blocks in
    '''
    blockList = []

    # determine block coordinate from lazor by looking at odd and even
    # coordinate positions
    for i in range(len(lazor_path)):
        for j in range(len(lazor_path[i])):
            if lazor_path[i][j][0] == 1:  # first position is a special case
                x = lazor_path[i][j][0]//2
                y = lazor_path[i][j][1]//2
                blockList.append([x, y])
            elif lazor_path[i][j][0] % 2 == 0:  # even
                x = lazor_path[i][j][0]//2
                y = lazor_path[i][j][1]//2
                blockList.append([x, y])
                blockList.append([x-1, y])
            else:
                x = lazor_path[i][j][0]//2
                y = lazor_path[i][j][1]//2
                blockList.append([x, y])
                blockList.append([x, y-1])

    # adjust the blocklist to match the format of other blocks (starting at 1)
    blockList = [[blockList[i][0]+1, blockList[i][1]+1] for i in range(len(blockList))]

    # find blocks that are in the path of the lazozr and are allowed blocks
    common_blocks = [list(x) for x in set(tuple(x) for x in blockList).intersection(set(tuple(x) for x in blocks_allowed))]
    # convert the coordinates to the coorelated numbers
    common_blocks_num = [coord_to_num(Grid, common_blocks[i]) for i in range(len(common_blocks))]

    return common_blocks_num


def refract_branches(lazor_path_list, lazor_dir_list, lazor_num):

    a = [tuple(lazor_path_list[lazor_num][i]) for i in range(len(lazor_path_list[lazor_num]))]
    frequency = Counter(a)
    points = list(frequency.keys())
    numbers = list(frequency.values())
    contact_list = []
    contact_list = [list(points[i]) for i in range(len(numbers)) if numbers[i] == 2]
    a = [list(a[i]) for i in range(len(a))]
    if len(lazor_path_list) > 1:
        for x in range(len(contact_list)):
            refract_index = [i for i in range(len(a)) if a[i] == contact_list[x]]
            parent = lazor_path_list[lazor_num][0:refract_index[0]]
            branch_1 = lazor_path_list[lazor_num][refract_index[0]:refract_index[1]]
            branch_2 = lazor_path_list[lazor_num][refract_index[1]:len(a)]
            parent_dir = lazor_dir_list[lazor_num][0:refract_index[0]]
            branch_1_dir = lazor_dir_list[lazor_num][0:refract_index[1]]
            branch_2_dir = parent_dir + lazor_dir_list[lazor_num][refract_index[1]:len(a)]
            branch = True
    else:
        parent = None
        branch_1 = None
        branch_2 = None
        branch_1_dir = None
        branch_2_dir = None
        branch = False

    return parent, branch_1, branch_2, branch_1_dir, branch_2_dir, branch


def change_refract_branches(branch_1, branch_2, branch_1_dir, branch_2_dir, contact_position):

    if contact_position in branch_1:

        return branch_2, branch_2_dir
    elif contact_position in branch_2:

        return branch_1, branch_1_dir
    return None, None


def block_behind_lazor(Lazor_Path,Lazor_Dir,Grid):
    r = len(Grid)
    c = len(Grid[0])

    blockList = []
    LP = []
    LD = []
    behind = []
    forward = []
    A = []

    for i in range(len(Lazor_Path)):
        LP.append(Lazor_Path[i][0])
        LD.append(Lazor_Dir[i][0])

    for i in range(len(LP)):
        if (LP[i][1] % 2) == 1:
            x = LP[i][0]//2
            y = (LP[i][1]+1)//2
            possible = [[x, y], [x+1, y]]

            for j in range(len(possible)):
                if 1 <= possible[j][0] <= c and 1 <= possible[j][1] <= r:
                    num = [coord_to_num(Grid, possible[j])]
                    A.extend(num)

            blockList.append(A)

            if len(blockList[i]) > 1:
                if LD[i][0] == -1:
                    behind_obj = blockList[i][1]
                    forward_obj = blockList[i][0]
                else:
                    behind_obj = blockList[i][0]
                    forward_obj = blockList[i][1]
            else:
                behind_obj = None
                forward_obj = blockList[i][0]

        elif (LP[i][0] % 2) == 1:
            x = (LP[i][0]+1)//2
            y = (LP[i][1])//2
            possible = [[x, y], [x, y+1]]

            for j in range(len(possible)):
                if 1 <= possible[j][0] <= c and 1 <= possible[j][1] <= r:
                    num = [coord_to_num(Grid, possible[j])]
                    A.extend(num)
            blockList.append(A)
            if len(blockList[i]) > 1:

                if LD[i][1] == -1:
                    behind_obj = blockList[i][1]
                    forward_obj = blockList[i][0]
                else:
                    behind_obj = blockList[i][0]
                    forward_obj = blockList[i][1]
            else:
                behind_obj = None
                forward_obj = blockList[i][0]

        behind.append(behind_obj)
        forward.append(forward_obj)
        A = []
        possible = []

    return behind, forward


def coord_to_num(Grid, coord):
    '''
    This function take in the grid and coordinate and assigns them the
    coorelating number values
        inputs
            Grid: list, lsit of grid
            coord: tuple, coordinate value
        outputs
            nums[index]: int, coorelating int
    '''
    r = len(Grid)
    c = len(Grid[0])

    dim = r*c

    coords = [[i+1, j+1] for j in range(r) for i in range(c)]
    nums = [i+1 for i in range(dim)]
    index = coords.index(coord)
    return nums[index]


def num_to_coord(Grid, num):
    '''
    This function take in the grid and numbers and assigns them the
    coorelating coordinate values
        inputs
            Grid: list, lsit of grid
            num: int, number to be converted into a tuple
        outputs
            coords[index]: tuple, coorelating coordinate value
    '''

    r = len(Grid)
    c = len(Grid[0])
    dim = r*c

    coords = [[j+1, i+1] for i in range(r) for j in range(c)]
    nums = [i+1 for i in range(dim)]

    index = nums.index(num)
    return coords[index]

def get_combos(Blocks, numList, common_blocks_num, Grid, behind, forward):
    '''
    This function takes in a list of block IDs and coordinate IDs and returns
    all of the possible combinations
        inputs
            Blocks: list, list of blocks
            numList: list of valid positions
            common_blocks_num: list of numbers in the path of the lazor
            Grid: lsit, the grid from the read file
            behind: tuple, block position behind the lazor
            forward: tuple, block position infront of the lazor
        outputs
            combos: nested list, list of all the possible combinations
    '''
    # use combinations and permutations
    a = list(permutations(Blocks, len(Blocks)))
    b = list(combinations(numList, len(Blocks)))
    combos_with_reps = []

    for i in range(len(a)):
        for j in range(len(b)):
            if any(x in common_blocks_num for x in b[j]):
                # check to make sure that we are not placing a block infront
                # and behind a lazor at the same time (which would remove the
                # lazor
                if (behind[0] not in b[j]) or (forward[0] not in b[j]):
                    combos_with_reps.append(a[i]+b[j])

    combos = list(set(combos_with_reps))
    return combos


def check_inside(x_dir,y_dir,contact_side):

    if contact_side == 1 and y_dir == -1:
        return True
    elif contact_side == 3 and x_dir == -1:
        return True
    elif contact_side == 2 and y_dir == 1:
        return True
    elif contact_side == 4 and x_dir == 1:
        return True
    else:
        return False
    