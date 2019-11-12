# Lazor-Project
Group Project for Software Carpentry
This project aimed to calculate the solution to various board arrangements from the game "lazors."

Files Included with Project:
  Block.py
  lazor_master_code.py
  Save_Solutions.py
  functions.py
  readFile.py
  
Strategy for Solving:
  For each lazor board, we generated all combinations of block positions possible. We then 
  iterated through these combinations. For each combination we calculated the corresponding
  lazor positions, and tested to see if the lazor posiions matched the lazor targets. If not
  the function continues to the next iteration
  
  The solution if then save to a text file and an image of the solved board is generated.
 
  
