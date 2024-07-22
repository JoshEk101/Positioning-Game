import numpy as np
import matplotlib.pyplot as plt
import random

def getCoordinates():
    xAxis = random.randint(1,4)
    yAxis = random.randint(1,4)
    playerOne = [xAxis, yAxis]
    xAxis = random.randint(1,4)
    yAxis = random.randint(1,4)
    playerTwo = [xAxis, yAxis]
    xAxis = random.randint(1,4)
    yAxis = random.randint(1,4)
    objectStone = [xAxis, yAxis]
    return (playerOne, playerTwo, objectStone)

def check_interception(A, B, C):
    x1, y1 = A
    x2, y2 = B
    x, y = C
    
    # Check for collinearity. Since this is a simple version, if the stone is not collinear,
    # then there is no way that the stone could interrupt the path of the two players. Essentially,
    # we are looking for one straight line.
    area = x1*(y2 - y) + x2*(y - y1) + x*(y1 - y2)
    if area != 0:
        return False 
    
    # This checks to see if the stone's coordinates lie between the players. Since we have
    # already checked that this is a straight line, if it turns out the stone's coordinates
    # lie between the two players, then we can say the path is interrupted.
    # This program also assumes that if we have collinearity, and the stone's coordinate is the 
    # same as a players, then the path is interrupted.
    if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
        return True
    else:
        return False


playerOne, playerTwo, objectStone = getCoordinates()

title = check_interception(playerOne, playerTwo, objectStone)

plt.xlim(0, 5)
plt.ylim(0, 5)
plt.grid()

plt.plot(playerOne, playerTwo, marker="o")
plt.plot(objectStone[0], objectStone[1], marker="o")

plt.title(title)
plt.show()


# plt.plot(playerOne[0], playerOne[1], marker="o")
# plt.plot(playerTwo[0], playerTwo[1], marker="o")



# import tkinter as tk
# from tkinter import ttk

# root = tk.Tk()
# root.geometry("200x200")
# root.resizable(0,0)

# root.columnconfigure(0, weight = 1)
# root.columnconfigure(1, weight = 3)

# username_label = ttk.Label(root, text="Username:")
# username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

# root.mainloop()