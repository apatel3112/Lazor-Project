# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 00:14:18 2019

@author: bento
"""

from PIL import Image, ImageDraw, ImageFont
from Block import Block
import io


def new_lazor_path(Lazor_Path):

    New_Lazor_Path = []
    for lazor in (Lazor_Path):
        repeated_points = [0]
        for i in range(1, len(lazor)):
            if abs((lazor[i][0]-lazor[i-1][0])) > 1 or abs((lazor[i][1]-lazor[i-1][1])) > 1:
                repeated_points.append(i)
        repeated_points.append(len(lazor))
        
        for i in range(1, len(repeated_points)):
            new_lazor = lazor[repeated_points[i-1]:repeated_points[i]]
            New_Lazor_Path.append(new_lazor)
    
    return New_Lazor_Path  
     
    


def save_file(file_name, Grid, blocks, Lazor_Path, P):
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
    '''
    file_name = file_name.replace('bff', 'txt')
    
    
    
    block_pos = []
    block_type = []
    for i in blocks:
        block_pos.append(i.pos())
        block_type.append(i.get_type())
        
    #print(block_pos)
    #print(block_type)    
    
    #convert Grid strings into lists
    for i in range(len(Grid)):
        Grid[i] = list(Grid[i])
         
    #replace grid elements with new block types
    solved_grid = Grid    
    for i in range(len(block_pos)):
        solved_grid[block_pos[i][1]-1][block_pos[i][0]-1] = block_type[i]
    
    
    #print(solved_grid)
    
    
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
    
    load_image(file_name, solved_grid, Lazor_Path, P)
    
def load_image(file_name, solved_grid, Lazor_Path, P, blocksize=120):
    
    #define size of the lazor board image
    width = len(solved_grid[0])*blocksize
    height = len(solved_grid)*blocksize
    Size = (width+5, height+5)
    
    #creat blank white image
    img = Image.new("RGB", Size, (255, 255, 255))
    with open("arialbd.ttf", "rb") as f:
        bytes_font = io.BytesIO(f.read())
    font = ImageFont.truetype(bytes_font, size=12)
    
    #loop through each element of the solved grid
    for i in range(len(solved_grid)):
        for j in range(len(solved_grid[0])):
            
            #for each element, color the correspinding block on the image a 
            #specific color
            if solved_grid[i][j] == 'reflect':
                for w in range(j*blocksize, (j+1)*blocksize):
                    for h in range(i*blocksize, (i+1)*blocksize):
                        img.putpixel((w, h), (179, 179, 179))
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
    
    
    
    
    Lazor_Start = []
    for i in Lazor_Path:
        Lazor_Start.append(i[0])
        
    for i in Lazor_Start:
        draw = ImageDraw.Draw(img)
        x = i[0]*blocksize/2
        y = i[1]*blocksize/2
        r = 3
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(255, 0, 0))
        
    draw = ImageDraw.Draw(img)    
    for x in range(len(solved_grid[0])+1):
        draw.line((x*blocksize, 0, x*blocksize, height),(0, 0, 0))
        
    for y in range(len(solved_grid)+1):
        draw.line((0, y*blocksize, width, y*blocksize),(0, 0, 0))
    
        
        
    
    New_Lazor_Path = new_lazor_path(Lazor_Path) 
    print(New_Lazor_Path)
    
    #draw a red line between every point on the lazor_path    
    for i in range(len(New_Lazor_Path)):
        for j in range(len(New_Lazor_Path[i])-1):
            x1 = New_Lazor_Path[i][j][0]
            y1 = New_Lazor_Path[i][j][1]
            x2 = New_Lazor_Path[i][j+1][0]
            y2 = New_Lazor_Path[i][j+1][1]  
            
            draw = ImageDraw.Draw(img)
            draw.line((x1*blocksize/2, y1*blocksize/2, x2*blocksize/2, y2*blocksize/2), (255, 0, 0))
            
    for i in P:
        draw = ImageDraw.Draw(img)
        x = i[0]*blocksize/2
        y = i[1]*blocksize/2
        r = 5
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(0, 0, 0))
        

    
                    
    file_name = file_name.replace("txt", "png")        
    #save image
    img.save("%s_%s" % ("solved", file_name))
                
    img.show() 
    
    
    
    
    