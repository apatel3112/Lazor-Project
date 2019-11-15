#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This class defines a block object and allows you to perform different
operations with this block
"""

class Block():

    def __init__(self, block_type, position):
        '''
        initializes the block
        input
           none
        output
            none
        '''
        self.block_type = block_type
        self.position = position

    def change_position(self, new_position):
        '''
        function that changes the position of the block
        input
            new position: new positon of the block
        output
            new block position
        '''
        self.position = new_position

        return new_position

    def get_type(self):
        '''
        function that returns the type of block that we have
        input
            none
        output
            block type
        '''
        return self.block_type

    def pos(self):
        '''
        function that returns the type of block that we have
        input
            none
        output
            block type
        '''
        return self.position

    def add_blocks(self, b):
        '''
        function that updates the b (block) matrix and identifies the potential
        spots for the lazor to hit
        input
            b: matrix: matrix of the blocks already placed
        output
            b: matrix: updated matrix of the blocks
        '''
        position = list(self.position)
        pos_x = position[0]
        pos_y = position[1]

        b[1+((pos_y-1)*2)][((pos_x-1)*2)] = 3  # left
        b[((pos_y-1)*2)][1+((pos_x-1)*2)] = 1  # top
        b[1+((pos_y-1)*2)][2+((pos_x-1)*2)] = 4  # right
        b[2+((pos_y-1)*2)][1+((pos_x-1)*2)] = 2  # bottom

        return b

    def b_matrix(self):
        '''
        The functions returns the block type and the coordinates of the
        surrounding coordinates that a lazor could hit
        Input
            none
        Output
            coords: list of block coordinates for one block
            b_type: type of block that we have
        '''
        position = list(self.position)
        pos_x = position[0]
        pos_y = position[1]

        b_type = self.block_type
        # getting the coordinates
        coords = [[(pos_x-1)*2, 1+((pos_y-1)*2)], [1+((pos_x-1)*2), (pos_y-1)*2], [2+((pos_x-1)*2), 1+((pos_y-1)*2)], [1+((pos_x-1)*2), 2+((pos_y-1)*2)]]
        return coords, b_type

    def block_prop(self, x_dir, y_dir, contact_side):
        '''
        The functions returns the new direction of the lazor and whether or not
        the lazor after the contact position should be deleted
        Input
            x_dir: int: x direction of lazor
            y_dir: int: y direction of lazor
            contact_side: int: value coorelating to the side of the block that
            was hit by the lazor
        Output
            new_x_dir: int: new x direction of the lazor
            new_y_dir: int: new y direction of the lazor
            delete_after_contact: boolean: if the lazor is deleted after
            contact
        '''
        # if statement to adjust the new direction based on the contact side
        if contact_side == 1 or contact_side == 2:
            new_x_dir, new_y_dir = x_dir, y_dir*-1
        elif contact_side == 3 or contact_side == 4:
            new_x_dir, new_y_dir = x_dir*-1, y_dir

        # if statmeent that determines if the rest of the lazor should be
        # deleted based on the block type
        if self.block_type == "opaque":
            delete_after_contact = True
        else:
            if self.block_type == "refract":
                delete_after_contact = False
            if self.block_type == "reflect":
                delete_after_contact = True

        return new_x_dir, new_y_dir, delete_after_contact
