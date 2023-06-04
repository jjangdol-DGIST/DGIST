from functions import *
import glob
import os
import numpy as np
import re
from functions import _main
# =============================
meanp = np.loadtxt('result.txt', delimiter=',')

while True:
    # =======================
    obj = "/home/dgist/2-1/ComputerVision/practice_blackwind/final_project/example_images/"
    name = input("Put the name of the image (If you want to quit, press Enter): ") # .png 빼고
    if name == '':
        break
    else:
        pass    
    obj = obj + name + ".png"
    # =======================
    df, decide = mdc(_main(obj).flatten(), meanp)
    if decide == 1:
        decide = 'Seonbin'
    else:
        decide = 'Ungi'
    print(f"The {name} is closer to {decide}.")

print("Good bye!")