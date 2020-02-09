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
        my_list = []
        hist = np.zeros(256)
        for i in range(0, img.shape[0]):#x 
            max_x = max(img[i])
            # curr_array = img[i]
            # curr_item = curr_array[8].index
            for j in range(0, img.shape[1]):#y
                hist[img[i,j]]+=1
            #print(my_list)
            

        #print(max_x)
        #print(curr_item)
        # print(curr[8])
        # print(prev)

        # print("this is i",i)
        # print("this is j",j)
        return hist

    hist = imhist(img)
    plt.plot(hist)
   # plt.show()
    before = time.time()
    #manual threshold
    img = threshold(img,max_x-50)
    #opencv threshold
    #t,img = cv.threshold(img,50,255,cv.THRESH_BINARY)
    after = time.time()
    print("Time taken to process hand coded thresholding: " + str(after-before))
    #cv.imshow('thresholded image 1',img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # smallest = img.min(axis=0).min(axis=0)
    # biggest = img.max(axis=0).max(axis=0)
    # print(smallest)

    # hist_max = cv.calcHist([img], [0], None, [256], [0, 256])
    # hist_max = [val[0] for val in hist] 
    #n, bins, patches = ax.hist(<your data>, bins=<num of bins>, normed=True, fc='k', alpha=0.3)
