'''
This file prompts user for a ppm images dirctory to process
Reads  the images and finds the average
Writes the average pixel image to a .pp file.
'''
# Driver functions imports
from genericpath import exists
import os

# Global Variables
rootDir = "raw_images"
orionDir = "orion"
coneNebulaDir = "cone_nebula"
n44fDir = "n44f"
wfc3_uvisDir = "wfc3_uvis"
chosenDir = ""
height = 0
width = 0
maxColor = 0
images = []
outFile = ""  # output file name
fileCount = 0  # keep count of files in a directory

# Prompt user for input choice
print("Which image set do you want to process?")
print(" 1) cone_nebula (The Cone Nebula - NGC 2264)")
print(" 2) n44f (Interstellar Bubble N44F)")
print(" 3) orion (The Orion Nebula)")
print(" 4) wfc3_uvis (Carina Nebula)")
selection = int(input(" Selection:"))


# use input to decide files to process
if selection == 1:
    # construct path to cone_nebula images
    chosenDir = os.path.join(rootDir, coneNebulaDir)
    # set output file name to cone_nebula
    outFile = coneNebulaDir
elif selection == 2:
    # construct path to n44f images
    chosenDir = os.path.join(rootDir, n44fDir)
    # set output file name to n44f
    outFile = n44fDir
elif selection == 3:
    # construct path to orion images
    chosenDir = os.path.join(rootDir, orionDir)
    # set output file name orion
    outFile = orionDir
elif selection == 4:
    # construct path to wfc3_uvis images
    chosenDir = os.path.join(rootDir, wfc3_uvisDir)
    # set output file name to wfc3_uvis
    outFile = wfc3_uvisDir
else:
    # handle invalid user input by quiting program
    print("Invalid Selection. Input Must be (1-4)")
    exit

# validation to check if file exist
if os.path.exists(chosenDir) and len(chosenDir) > 4:

    # loop the file directory and add every filename into a list
    for(root, dir, files) in os.walk(chosenDir, topdown=True):
        for file in files:
            # increment file count for every file in the directory
            fileCount += 1

            # open file to read the lines
            file = open(os.path.join(chosenDir, file), 'r')
            lines = file.readlines()
            image = []
            for i, line in enumerate(lines):
                # read the ppm file header section i.e. lines 0-2
                if i == 1:
                    line = line.split()
                    listMap = map(int, line)
                    listNums = list(listMap)
                    width = listNums[0]  # image width
                    height = listNums[1]  # image height
                if i == 2:
                    color = line.strip()
                    maxColor = int(color)  # max image color
                # read out the image pixels RGB values line by line
                if i >= 3:
                    line = line.strip()
                    line = line.split()
                    listMap = map(int, line)
                    listNums = list(listMap)
                    # create a list containing an image RGB pixel values
                    for i in range(len(listNums)):
                        image.append(listNums[i])
            # add all images into the images list and find sum of coresponding image pixels
            if len(images) == 0:
                images = image
            else:
                templist = [x + y for x, y in zip(images, image)]
                images = templist
else:
    print("Internal Error")
    exit
# find average of the image pixels by dividing every element on the pixel sums list by total files in the directory
imagesAvg = [x / fileCount for x in images]

# find new maximum color used in the average
newMaxColor = int(max(imagesAvg))
# breakdown the list of avarages into RGB sublists, rows
imgRGBList = [imagesAvg[x:x+3] for x in range(0, len(imagesAvg), 3)]

# open a .ppm file to write the processed result. Creates file if it does not exist
finalImg = open(outFile+".ppm", "w")

# write header
finalImg.write("P3")
finalImg.write("\n")
finalImg.write(str(width))
finalImg.write(" ")
finalImg.write(str(height))
finalImg.write("\n")
finalImg.write(str(newMaxColor))
finalImg.write("\n")

# append image average RGB values to file
for sublist in imgRGBList:
    vals = str(int(sublist[0])) + " " + \
        str(int(sublist[1]))+" " + str(int(sublist[2])) + "\n"
    finalImg.write(vals)

# close file
finalImg.close()
