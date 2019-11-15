#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file test some of the main functions in the functions file of our code
"""
import unittest
import functions


class TestStringMethods(unittest.TestCase):

    def test_combos(self):
        '''
        Function ensures that the proper combos are being output from the
        combos function
        '''
        Blocks = ["R", "B"]
        numList = [i for i in range(1, 4)]
        common_blocks_num = [1, 2]
        Grid = ['oooo', 'oooo', 'oooo', 'oooo']
        combos = [('B', 'R', 2, 3), ('B', 'R', 1, 2), ('R', 'B', 1, 2), ('R', 'B', 2, 3)]
        behind =  [1, 4]
        forward = [3, 8]
        self.assertEqual(functions.get_combos(Blocks, numList, common_blocks_num, Grid, behind, forward), combos)

    def test_num_to_coord(self):
        '''
        Function ensures that the proper coordinates are being output from the
        num to coord function
        '''
        Grid = ['oooo', 'oooo', 'oooo', 'oooo']
        self.assertEqual(functions.num_to_coord(Grid, 5), [1, 2])

    def test_coord_to_num(self):
        '''
        Function ensures that the proper numbers are being output from the
        coord to num function
        '''
        Grid = ['oooo', 'oooo', 'oooo', 'oooo']
        self.assertEqual(functions.coord_to_num(Grid, [1, 2]), 5)

    def test_change_refract_branches(self):
        '''
        Function ensures that the proper output is coming from the
        change_refract_branches function and that if there is no branch,
        none is output
        '''
        branch_1 = [1, 1], [2, 2], [3, 3]
        branch_2 = [2, 2], [3, 1], [4, 0]
        branch_1_dir = [1, 1], [1, 1], [1, 1]
        branch_2_dir = [1, -1], [1, -1], [1, -1], [1, -1]
        contact_position = [2, 2]
        self.assertEqual(functions.change_refract_branches(branch_1, branch_2, branch_1_dir, branch_2_dir, contact_position), ((branch_2), (branch_2_dir)))
        self.assertEqual(functions.change_refract_branches(branch_1, branch_2, branch_1_dir, branch_2_dir, [3, 1]), ((branch_1), (branch_1_dir)))
        self.assertEqual(functions.change_refract_branches(branch_1, branch_2, branch_1_dir, branch_2_dir, [2, 7]), (None, None))

    def test_refract_branches(self):
        '''
        Function ensures that the proper output is coming from the
        refract_branches function and that if there is no branch,
        none is output
        '''
        lazor_path_list = [[[7, 2], [6, 3], [5, 4], [5, 4], [4, 5]]]
        lazor_dir_list = [[[-1, 1], [-1, 1], [-1, 1], [1, -1], [-1, 1]]]
        lazor_num = 0
        self.assertEqual(functions.refract_branches(lazor_path_list, lazor_dir_list, lazor_num), (None, None, None, None, None, False))

    def test_valid_positions(self):
        '''
        Function ensures that the proper valid positions is coming from
        the valid position function
        '''
        lazor_path = [[[7, 2], [6, 3], [5, 4], [4, 5]]]
        blocks_allowed = [[1, 4], [3, 3], [2, 3], [4, 1]]
        Grid = ['oooo', 'oooo', 'oooo', 'oooo']
        self.assertEqual(functions.valid_positions(lazor_path, blocks_allowed, Grid), [4, 11, 10])

    def test_lazor_contact_tuple(self):
        '''
        Function ensures that the proper output comes from teh lazor contact
        tuple function
        '''
        m = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 2],
              [0, 0, 0, 0, 0, 0, 0, 2, 0],
              [0, 0, 0, 0, 0, 0, 2, 0, 0],
              [0, 0, 0, 0, 0, 2, 0, 0, 0],
              [0, 0, 0, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 2, 0, 0, 0, 0, 0],
              [0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        b = [[0, 1, 0, 0, 0, 0, 0, 0, 0],
              [3, 0, 4, 0, 0, 0, 0, 0, 0],
              [0, 2, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 3, 0, 4, 0, 0, 0, 0],
              [0, 0, 0, 2, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 3, 0, 4],
              [0, 0, 0, 1, 0, 0, 0, 2, 0],
              [0, 0, 3, 0, 4, 0, 0, 0, 0],
              [0, 0, 0, 2, 0, 0, 0, 0, 0]]

        lazor_path_list = [[[2, 7], [3, 6], [4, 5], [5, 4], [6, 3], [7, 2], [8, 1]]]
        lazor_dir_list = [[[1, -1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1]]]
        lazor_num = 0
        used_contact_pos = []
        total_laze = 1
        self.assertEqual(functions.lazor_contact_tuple(m, b, lazor_path_list, lazor_dir_list, lazor_num, used_contact_pos, total_laze), ([2, 7], 1, -1, 0, 3, [[2, 7], [3, 6]], [[2, 7]], [[2, 7], [3, 6]]))


if __name__ == '__main__':

    unittest.main()
