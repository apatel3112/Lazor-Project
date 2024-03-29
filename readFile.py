#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anusha Patel, Ben Toler, Madeline Noble

This file contains functions that read the BFF file and converts the
information into matricies and lists that the solver can use
"""
import numpy as np
from Block import Block


def read_file(file_name):
    '''
        this function reads the file and outputs corresponding matricies
        input
            file_name: string: name of the file to be read
        output
            Blocks
            Lazor_Path: nested list: list with all of the lazor paths
            Lazor_Dir: nested list: list with all of the directions
            m: matrix for the lazor, 2s represent lazor path
            b: matrix with for the blocks
            not_allowed: list: positions that no blocks are allowed in
            t: matrix: matrix with all of the targets that the lazor need to
                hit
    '''
    Grid = []  # raw grid from the read in file
    A = 0  # number of reflect blocks
    B = 0  # number of opqaue blocks
    C = 0  # number of refrect blocks
    P = []  # list of target position coordinates
    L = []  # lazor information

    file = open(file_name, "r")
    lines = file.readlines()
    # these for loops read and process the input file accordingly
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

    # create empty matrices based on grid size
    row = len(Grid)
    col = len(Grid[0])

    m = []
    for i in range(len(L)):
        c = np.zeros((2*row+1, 2*col+1), dtype=int)
        m.append(c)

    b = np.zeros((2*row+1, 2*col+1), dtype=int)
    t = np.zeros((2*row+1, 2*col+1), dtype=int)

    # read fixed blocks and non permitted positions
    # fixed blocks corresponds to pos_x-1 and pos_y-1
    fixed_blocks_raw = [[i, j] for i in range(len(Grid[0])) for j in range(len(Grid)) if Grid[j][i] == 'B' or Grid[j][i] == 'A' or Grid[j][i] == 'C']
    fixed_Blocks = []

    # initializes the fixed blocks
    for i in range(len(fixed_blocks_raw)):
        if Grid[fixed_blocks_raw[i][1]][fixed_blocks_raw[i][0]] == 'B':
            i = Block("opaque", (fixed_blocks_raw[i][1], fixed_blocks_raw[i][0]))
            fixed_Blocks.append(i)
        elif Grid[fixed_blocks_raw[i][1]][fixed_blocks_raw[i][0]] == 'A':
            i = Block("reflect", (fixed_blocks_raw[i][1], fixed_blocks_raw[i][0]))
            fixed_Blocks.append(i)
        elif Grid[fixed_blocks_raw[i][1]][fixed_blocks_raw[i][0]] == 'C':
            i = Block("reflect", (fixed_blocks_raw[i][1], fixed_blocks_raw[i][0]))
            fixed_Blocks.append(i)

    Lazor_Path = []
    Lazor_Dir = []
    Lazor_Path_i = []
    Lazor_Dir_i = []

    # create empty matrices based on grid size
    row = len(Grid)
    col = len(Grid[0])

    m = []
    for i in range(len(L)):
        c = np.zeros((2*row+1, 2*col+1), dtype=int)
        m.append(c)

    b = np.zeros((2*row+1, 2*col+1), dtype=int)
    t = np.zeros((2*row+1, 2*col+1), dtype=int)

    # read fixed blocks and non permitted positions
    # fixed blocks corresponds to pos_x-1 and pos_y-1
    fixed_blocks = [[i, j] for i in range(len(Grid[0])) for j in range(len(Grid)) if Grid[j][i] == 'B' or Grid[j][i] == 'A' or Grid[j][i] == 'C']

    # adds fixed blocks to the b matrix
    for x in range(len(fixed_blocks)):
        b[1+((fixed_blocks[x][1])*2)][((fixed_blocks[x][0])*2)] = 1
        b[((fixed_blocks[x][1])*2)][1+((fixed_blocks[x][0])*2)] = 1
        b[1+((fixed_blocks[x][1])*2)][2+((fixed_blocks[x][0])*2)] = 1
        b[2+((fixed_blocks[x][1])*2)][1+((fixed_blocks[x][0])*2)] = 1

    # adds possions to the b matrix not accessible to matrix
    not_allowed = [[i, j] for i in range(len(Grid[0])) for j in range(len(Grid)) if Grid[j][i] == 'x']

    for y in range(len(not_allowed)):
        b[1+((not_allowed[y][1])*2)][((not_allowed[y][0])*2)] = -1
        b[((not_allowed[y][1])*2)][1+((not_allowed[y][0])*2)] = -1
        b[1+((not_allowed[y][1])*2)][2+((not_allowed[y][0])*2)] = -1
        b[2+((not_allowed[y][1])*2)][1+((not_allowed[y][0])*2)] = -1

    # return vector of positions x and y not allowed to place blocks
    not_allowed.extend(fixed_blocks)
    
    # create vectors for x and y directions if more than 1 Lazor
    j = []
    k = []
    count_j = []
    count_k = []

    # lazor direction
    for i in range(len(L)):
        j.append(L[i][2])
        k.append(L[i][3])
        count_j.append(L[i][0])
        count_k.append(L[i][1])

    # Add lazor path on matrix m
    for i in range(len(L)):
        Lazor_Path_i.append([count_j[i], count_k[i]])
        Lazor_Dir_i.append([j[i], k[i]])

        while 0 <= count_k[i] < 2*row+1 and 0 <= count_j[i] < 2*col+1:
            m[i][count_k[i]][count_j[i]] = 2
            count_j[i] += j[i]
            count_k[i] += k[i]
            Lazor_Path_i.append([count_j[i], count_k[i]])
            Lazor_Dir_i.append([j[i], k[i]])

        Lazor_Dir_i.pop()
        Lazor_Path_i.pop()

        Lazor_Path.append(Lazor_Path_i)
        Lazor_Dir.append(Lazor_Dir_i)

        Lazor_Path_i = []
        Lazor_Dir_i = []

    # Add targets to matrix m
    P = list(P)
    for i in range(len(P)):
        t[P[i][1]][P[i][0]] = 1

    Blocks = [A, B, C]

    return Grid, fixed_Blocks, Blocks, Lazor_Path, Lazor_Dir, m, b, not_allowed, t, P
