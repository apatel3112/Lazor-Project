#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 00:33:35 2019

@author: madelinenoble
"""

"""
Created on Tue Nov 12 00:14:18 2019
@author: bento
"""

from PIL import Image, ImageDraw

def save_file(file_name, Grid, block_pos, block_type, Lazor_Path):
    '''
    This function creates the solved grid and writes it to a txt file
    
    Inputs:
        file_name
        Grid: orgiinal lazor grid
        block_pos: the solved positions of each block in the lazor file
        block_type: the type of each block. index of block ype corresponds
        to index of block pos
        
    Outputs:
        solved_grid: Grid with solved blokc placements
        new file: solved grid written to a txt file
        image: Image of solved lazor board
    '''
    file_name = file_name.replace('bff', 'txt')
    
    #convert Grid strings into lists
    for i in range(len(Grid)):
        Grid[i] = list(Grid[i])
         
    #replace grid elements with new block types
    solved_grid = Grid    
    for i in range(len(block_pos)):
        solved_grid[block_pos[i][0]-1][block_pos[i][1]-1] = block_type[i]
    
    #specidy solved file name from old file name
    new_file_name = "%s_%s" % ("solved", file_name)
    
    #open new file under as new_file_name and assign it to variable new_file
    new_file = open(new_file_name, "w+")
    
    
    #write each element of solved grid onto a new line in the new fiel
    for line in solved_grid:
        new_file.write("%s/n" % line)
        
        
    #close the new file    
    new_file.close()
    
    
    file_name = file_name.replace("txt", "png")
    
    load_image(file_name, solved_grid, Lazor_Path)
    
def load_image(file_name, solved_grid, Lazor_Path, blocksize=100):
    
    #define size of the lazor board image
    width = len(solved_grid[0])*blocksize
    height = len(solved_grid)*blocksize
    Size = (width, height)
    
    #creat blank white image
    img = Image.new("RGB", Size, (255, 255, 255))
    
    #Opaque = Blacko
    #Reflect = Gray
    #Refract = Light Blue
    #None_allowed = Red
    #Open = White
    
    
    #loop through each element of the solved grid
    for i in range(len(solved_grid)):
        for j in range(len(solved_grid[0])):
            
            #for each element, color the correspinding block on the image a 
            #specific color
            if solved_grid[i][j] == 'reflect':
                for w in range(j*blocksize, (j+1)*blocksize):
                    for h in range(i*blocksize, (i+1)*blocksize):
                        img.putpixel((w, h), (220, 220, 220))
            if solved_grid[i][j] == 'opaque':
                for w in range(j*blocksize, (j+1)*blocksize):
                    for h in range(i*blocksize, (i+1)*blocksize):
                        img.putpixel((w, h), (0, 0, 0))
            if solved_grid[i][j] == 'refrect':
                for w in range(j*blocksize, (j+1)*blocksize):
                    for h in range(i*blocksize, (i+1)*blocksize):
                        img.putpixel((w, h), (224, 255, 255))
            if solved_grid[i][j] == '0':
                for w in range(j*blocksize, (j+1)*blocksize):
                    for h in range(i*blocksize, (i+1)*blocksize):
                        img.putpixel((w, h), (255, 0, 0))
    
    #draw a red line between every point on the lazor_path    
    for i in range(len(Lazor_Path)):
        for j in range(len(Lazor_Path[0])-1):
            x1 = Lazor_Path[i][j][0]
            y1 = Lazor_Path[i][j][1]
            x2 = Lazor_Path[i][j+1][0]
            y2 = Lazor_Path[i][j+1][1]  
            
            draw = ImageDraw.Draw(img)
            draw.line((x1*blocksize/2, y1*blocksize/2, x2*blocksize/2, y2*blocksize/2), (255, 0, 0))
                    
    file_name = file_name.replace("txt", "png")        
    #save image
    img.save("%s_%s" % ("solved", file_name))
    