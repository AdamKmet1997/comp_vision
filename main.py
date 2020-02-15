import cv2 as cv
import numpy as np
import time
import matplotlib.pyplot as plt

#read in an image into memory
for folderout in range(1, 2):
    img = cv.imread('Oring'+str(folderout)+'.jpg',0)
    copy = img.copy()
    max_x = 0
    #print(folderout)
         
    def threshold(img,thresh):
        #implement thresholding ourselves using loops (soooo slow in python)
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                if img[i,j] > thresh:
                    img[i,j] = 255
                else:
                    img[i,j] = 0

        return img

    def imhist(img):
        global max_x
        hist = np.zeros(256)
        for i in range(0, img.shape[0]):#x 
            max_x = max(img[i])
            for j in range(0, img.shape[1]):#y
                hist[img[i,j]]+=1
        return hist
    
    structure =[[1, 1, 1],
                [1, 0, 1],
                [1, 1, 1]]

    def dilation(img):
        new_copy = img.copy()
        global max_x
        thresh = max_x -50
        hist = np.zeros(256)
        for i in range(0, img.shape[0]):#x 
            for j in range(0, img.shape[1]):#y
        # find if any of i-1, i+1, j-1, j+1 are 0
                if img[i,j] == 0:
                    for x in range(-1,2):
                        for y in range(-1,2):
                            if structure[x+1][y+1] == 1:
                                if  y != 0 and x != 0 and i + x >= 0 and i+ x < img.shape[0] and j + y >= 0 and j + y < img.shape[1] and  img[i+x][j+y]==255:
                                    #if i + x >= 0 and i+ x < img.shape[0] and j + y >= 0 and j + y < img.shape[1] and  img[i+x][j+y]==0:
                                    # if img[i+x][j+y] == 255:

                                    new_copy[i,j]=0

                # if img[i,j] == 255 and i - 1 >= 0 and i + 1 < img.shape[0] and j - 1 >= 0 and j + 1 < img.shape[1]:
                #     if img[i - 1, j] == 0 or img[i + 1, j] == 0 or img[i, j-1] == 0 or img[i, j+1] == 0 or img[i -1, j-1] == 0 or img[i -1 , j+1] == 0 or img[i + 1, j-1] == 0 or img[i + 1, j+1] == 0:
                #         new_copy[i,j] = 0
        #print(img)

        #if img[ i, j ] is 25 black
        #loop through structure - 1 to 2 for x here
        #same for y
        #if structure x +1 and y+1 is 1
        #if if structure i +1 and j+1 is 1
        #assign 255 to the img[i+1][j+1]==255
        return new_copy

    def erosion(img):
        new_copy = img.copy()
        global max_x
        thresh = max_x -50
        hist = np.zeros(256)
        for i in range(0, img.shape[0]):#x 
            for j in range(0, img.shape[1]):#y
        # find if any of i-1, i+1, j-1, j+1 are 0
                if img[i,j] == 0 and i - 1 >= 0 and i + 1 < img.shape[0] and j - 1 >= 0 and j + 1 < img.shape[1]:
                    if img[i - 1, j] == 255 or img[i + 1, j] == 255 or img[i, j-1] == 255 or img[i, j+1] == 255 or img[i -1, j-1] == 255 or img[i -1 , j+1] == 255 or img[i + 1, j-1] == 255 or img[i + 1, j+1] == 255:
                        new_copy[i,j] = 255
        #print(img)
        return new_copy

    def closing(img):
        dil = dilation(img)
        ero = erosion(dil)
        return ero

    


    hist = imhist(img) 
    img = threshold(img,max_x-50)#this makes everything either 0 or 255
    img = dilation(img)
    # img =erosion(img)
    #img = closing(img)

    hist = imhist(img)
    plt.plot(hist)
    #plt.show()
    print("max x axis value is = ",max_x)



    cv.imshow('thresholded image 1',img)
    cv.waitKey(0)
    cv.destroyAllWindows()
