#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 00:14:18 2019
@author: bento
"""
from PIL import Image, ImageDraw, ImageFont
from Block import Block
import io


def new_lazor_path(Lazor_Path):
    '''
    Thsi function breaks the solved lazor_path into a list of lists which has
    elements that differ by onnly one in either the x or y direction
    
    Inputs:
        lazor_path: solved lazor path from solver function. Length equal to
        number of lazors
    Oututs:
        New_lazor_Path: lazor path used in load image
    '''
    # define new lazor path vairable
    New_Lazor_Path = []
    # loop through each lazor of origiinal lazor path list
    for lazor in (Lazor_Path):
        # initialize repeates_points vairable with the first index position
        repeated_points = [0]
        # loop throguh each element of the lazor list
        for i in range(1, len(lazor)):
            # if a lazor positon changes by more than one from its previous point
            # then that index position is added to repeated points
            if abs((lazor[i][0]-lazor[i-1][0])) > 1 or abs((lazor[i][1]-lazor[i-1][1])) > 1:
                repeated_points.append(i)
        # end repeated_points with the final index position of teh lazor
        repeated_points.append(len(lazor))

        # break each lazor down into lists between each repeated_postioin index
        # and add each list to new lazor path variable

        for i in range(1, len(repeated_points)):
            new_lazor = lazor[repeated_points[i-1]:repeated_points[i]]
            New_Lazor_Path.append(new_lazor)


    #return new lazor path variable

    return New_Lazor_Path


def save_file(file_name, Grid, blocks, Lazor_Path, P):
    '''
    This function processes the input and opens a new png file to write in
    and calls the function to create the png
    Inputs:
        file_name
        Grid: orgiinal lazor grid
        block_pos: the solved positions of each block in the lazor file
        block_type: the type of each block. index of block ype corresponds
        to index of block pos
        P: positions where the fixed blocks
    Outputs:
        None
    '''
    file_name = file_name.replace('bff', 'txt')
    # define the final block position and type variable
    block_pos = []
    block_type = []

    # loop through each block object and load its postiion and type into their
    # respective vriables

    for i in blocks:
        block_pos.append(i.pos())
        block_type.append(i.get_type())

    # convert Grid strings into lists
    for i in range(len(Grid)):
        Grid[i] = list(Grid[i])

    # replace grid elements with new block types
    solved_grid = Grid
    for i in range(len(block_pos)):
        solved_grid[block_pos[i][1]-1][block_pos[i][0]-1] = block_type[i]

    # specidy solved file name from old file name
    new_file_name = "%s_%s" % ("solved", file_name)

    # open new file under as new_file_name and assign it to variable new_file
    new_file = open(new_file_name, "w+")

    # write each element of solved grid onto a new line in the new field
    for line in solved_grid:
        new_file.write("%s/n" % line)

    # close the new file
    new_file.close()
    file_name = file_name.replace("txt", "png")


    # convert the solved grid into an iamge of the solved board
    load_image(file_name, solved_grid, Lazor_Path, P)


def load_image(file_name, solved_grid, Lazor_Path, P, blocksize=120):
    '''
    This function creates png file by defining the pixels
    Inputs:
        file_name: string, name of the file to be saved
        solved_grid: list, grid with the cooresponding solution
        Lazor_Path: list, final lazor path
        P: positions of lazor targets
        blocksize=120
    Outputs:
        image od solved board
    '''
    # define size of the lazor board image
    width = len(solved_grid[0])*blocksize
    height = len(solved_grid)*blocksize
    Size = (width+5, height+5)

    # creat blank white image
    img = Image.new("RGB", Size, (255, 255, 255))
    # define font style and size for block descriptions
    with open("arialbd.ttf", "rb") as f:
        bytes_font = io.BytesIO(f.read())
    font = ImageFont.truetype(bytes_font, size=12)
    
    # loop through each element of the solved grid
    for i in range(len(solved_grid)):
        for j in range(len(solved_grid[0])):
            
            # for each element, color the correspinding block on the image a 
            # specific color and label it with text that describes its type
            if solved_grid[i][j] == 'reflect':
                for w in range(j*blocksize, (j+1)*blocksize):
                    for h in range(i*blocksize, (i+1)*blocksize):
                        img.putpixel((w, h), (169, 169, 169))
                draw = ImageDraw.Draw(img)
                draw.text((j*blocksize+20, (i+0.5)*blocksize-7), "Reflect Block", fill=(0, 0, 0), font=font)
            if solved_grid[i][j] == 'opaque':
                for w in range(j*blocksize, (j+1)*blocksize):
                    for h in range(i*blocksize, (i+1)*blocksize):
                        img.putpixel((w, h), (0, 0, 0))
                draw = ImageDraw.Draw(img)
                draw.text((j*blocksize+20, (i+0.5)*blocksize-7), "Opaque Block", fill=(255, 255, 255), font=font)
            if solved_grid[i][j] == 'refract':
                for w in range(j*blocksize, (j+1)*blocksize):
                    for h in range(i*blocksize, (i+1)*blocksize):
                        img.putpixel((w, h), (220, 220, 220))
                draw = ImageDraw.Draw(img)
                draw.text((j*blocksize+20, (i+0.5)*blocksize-7), "Refract Block", fill=(0, 0, 0), font=font)
            if solved_grid[i][j] == 'x':
                for w in range(j*blocksize, (j+1)*blocksize):
                    for h in range(i*blocksize, (i+1)*blocksize):
                        img.putpixel((w, h), (255, 255, 255))
                draw = ImageDraw.Draw(img)
                draw.text((j*blocksize+11, (i+0.5)*blocksize-7), "No Block Allowed", fill=(0, 0, 0), font=font)
                
    # define the start point of each lazor          
    Lazor_Start = []
    for i in Lazor_Path:
        Lazor_Start.append(i[0])
        
    # mark each lazor start position with a red dot
    for i in Lazor_Start:
        draw = ImageDraw.Draw(img)
        x = i[0]*blocksize/2
        y = i[1]*blocksize/2
        r = 3
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(255, 0, 0))
    
    # draww black grid on image to separate blocks    
    draw = ImageDraw.Draw(img)
    for x in range(len(solved_grid[0])+1):
        draw.line((x*blocksize, 0, x*blocksize, height), (0, 0, 0))

    for y in range(len(solved_grid)+1):
        draw.line((0, y*blocksize, width, y*blocksize), (0, 0, 0))

    # define new lazor path using new_lazor_path function
    New_Lazor_Path = new_lazor_path(Lazor_Path)

    # draw a red line between every point on the lazor_path
    for i in range(len(New_Lazor_Path)):
        for j in range(len(New_Lazor_Path[i])-1):
            x1 = New_Lazor_Path[i][j][0]
            y1 = New_Lazor_Path[i][j][1]
            x2 = New_Lazor_Path[i][j+1][0]
            y2 = New_Lazor_Path[i][j+1][1]
            draw = ImageDraw.Draw(img)
            draw.line((x1*blocksize/2, y1*blocksize/2, x2*blocksize/2, y2*blocksize/2), (255, 0, 0))
    
    # mark lazor targets as black dots
    for i in P:
        draw = ImageDraw.Draw(img)
        x = i[0]*blocksize/2
        y = i[1]*blocksize/2
        r = 5
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(0, 0, 0))

    file_name = file_name.replace("txt", "png")

    # save image
    img.save("%s_%s" % ("solved", file_name))
    img.show()
