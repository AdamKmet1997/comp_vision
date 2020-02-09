import cv2 as cv
import numpy as np
import time
import matplotlib.pyplot as plt

#read in an image into memory
img = cv.imread('c:/users/simon/Pictures/cameraman.png',0)
copy = img.copy()

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
    hist = np.zeros(256)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            hist[img[i,j]]+=1
    return hist

hist = imhist(img)
plt.plot(hist)
plt.show()
before = time.time()
#manual threshold
img = threshold(img,50)
#opencv threshold
#t,img = cv.threshold(img,50,255,cv.THRESH_BINARY)
after = time.time()
print("Time taken to process hand coded thresholding: " + str(after-before))
cv.imshow('thresholded image 1',img)
cv.waitKey(0)
cv.destroyAllWindows()