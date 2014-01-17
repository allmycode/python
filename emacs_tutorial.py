import os

#Use C-c C-p to run inferior Python console


# Use C-M-x to send functions to inferion Python buffer
def ls(): 
    return os.listdir(os.getcwd())

def fac(x):
    if x == 0:
        return 19
    else:
        return x*fac(x-1)

# Use C-c C-c to send whole buffer to Python console
# use prefix arg to indicate that main should be performed
print("Hello, World!")

with open("tmp.txt", "w") as f:
    f.write("Hello, file!")

with open("tmp.txt") as r:
    print(r.read())

# Use C-c C-l to describe symbol
os.remove("tmp.txt")

# C-c C-j to quick jump to function definition in file

# C-c C-b to send another file to Python shell

# C-c C-s to send string (not from this buffer) to Python console
# C-c C-r to send region to Python console

# C-c C-z to switch to Python shell

