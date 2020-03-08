import cv2 as cv
import numpy as np
import time
import matplotlib.pyplot as plt

#read in an image into memory
for folderout in range(1,16  ):# sets the range to 16 to open all the files 
    img = cv.imread('Oring'+str(folderout)+'.jpg',0)# read in the files in order
    copy = img.copy()
    max_x = 0
         
    def threshold(img,thresh):
        #implement thresholding ourselves using loops (soooo slow in python)
        for i in range(0, img.shape[0]):#loop through img x
            for j in range(0, img.shape[1]):#loop through img y
                if img[i,j] > thresh:#if the curr image pix is bigger than threshold 
                    img[i,j] = 255# make it white 
                else:
                    img[i,j] = 0# else make it black

        return img
    #this method makes the histogram
    def imhist(img):
        global max_x
        hist = np.zeros(256)
        for i in range(0, img.shape[0]):#x 
            max_x = max(img[i])#loop through the pixels and get the max x value which is basically th biggest peak
            for j in range(0, img.shape[1]):#y
                hist[img[i,j]]+=1
        return hist
    
    structure =[[1, 1, 1],# im using this structure as an example of perfect structure 
                [1, 0, 1],
                [1, 1, 1]]

    def dilation(img):
        new_copy = img.copy()# creates a copy of the image 
        global max_x#imports the threshold 
        thresh = max_x -50# minus 50 as it works perfect on all the examples 
        hist = np.zeros(256)
        for i in range(0, img.shape[0]):#x 
            for j in range(0, img.shape[1]):#y
        # find if any of i-1, i+1, j-1, j+1 are 0
                if img[i,j] == 0:# if the pixel is black
                    for x in range(-1,2):# looping through the structure x
                        for y in range(-1,2):#looping through the structure y
                            #checking all the neighbours of the image with the comparison of the with th structure
                                 if  x != 0 and y != 0 and i + x >= 0 and i+ x < img.shape[0] and j + y >= 0 and j + y < img.shape[1] and  img[i+x][j+y]==255:
                                    if i + x >= 0 and i+ x < img.shape[0] and j + y >= 0 and j + y < img.shape[1] and  img[i+x][j+y]==255:
                                        new_copy[i + x][j + y] =0# save the new information in the copy of the image 
        return new_copy#returning the copy of the image and not image it self 

    def erosion(img):
        new_copy = img.copy()# makes a copy of image 
        global max_x
        thresh = max_x -50# minus 50 as it works perfect on all the examples
        hist = np.zeros(256)
        for i in range(0, img.shape[0]):#x 
            for j in range(0, img.shape[1]):#y
                #checking all the neighbours of the pixel and checking for its values 
                if img[i,j] == 0 and i - 1 >= 0 and i + 1 < img.shape[0] and j - 1 >= 0 and j + 1 < img.shape[1]:
                    if img[i - 1, j] == 255 or img[i + 1, j] == 255 or img[i, j-1] == 255 or img[i, j+1] == 255 or img[i -1, j-1] == 255 or img[i -1 , j+1] == 255 or img[i + 1, j-1] == 255 or img[i + 1, j+1] == 255:
                        new_copy[i,j] = 255
        return new_copy#returning the copy of the image and not image it self 

    #this method combines the dilation and erosion together
    def closing(img):
        dil = dilation(img)
        ero = erosion(dil)
        return ero # retuns erosion because thats the last needed thing 

    def labeling(img):# here i put labels on the copy of the image array to find new areas 
        li = [[ 0 for i in range(0, img.shape[0])] for j in range(0, img.shape[1])]# creeate a copy ith all vals = 0
        counter = 1 # set counter start at 1
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                if img[i,j] == 0 and li[i][j] == 0:#if  curr pix is black
                    li[i][j] = counter
                    queue = []
                    queue.append([i,j])#added curr pixel to the queue
                    #
                    while len(queue)>0:# while the length is bigger than 0
                        pixel = queue.pop(0)
                        # following ifs check if neighbours around curr are black if yes add to queue to be checked next 
                        #add it to the li as 1 if this is the first area im looking at with black pixel

                        if img[pixel[0] -1,pixel[1]]==0 and li[pixel[0] -1][pixel[1]]==0:
                            queue.append([pixel[0] -1 , pixel[1]])
                            li[pixel[0] -1 ][ pixel[1]] = counter
                        if img[pixel[0] +1 , pixel[1]]==0 and li[pixel[0] +1 ][ pixel[1 ]]==0:
                            queue.append([pixel[0] +1 , pixel[1]])
                            li[pixel[0] +1 ][ pixel[1 ]] = counter
                        if img[pixel[0] , pixel[1] -1]==0 and li[pixel[0] -1 ][ pixel[1 ]-1]==0:
                            queue.append([pixel[0] , pixel[1]-1])
                            li[pixel[0] ][ pixel[1 ]-1] = counter
                        if img[pixel[0], pixel[1]+1]==0 and li[pixel[0] ][ pixel[1 ]+1]==0:
                            queue.append([pixel[0], pixel[1]+1])
                            li[pixel[0] ][ pixel[1 ]+1] = counter  
                    counter +=1# else increment the counter and start now labeling as 2 and so on
        return li# return the copy label list 

    def painting (img): #painting different aroeas in defferent colur to show difference 
        new_copy = img.copy()
        labels = labeling(img)
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                if labels[i][j] == 1:#if  curr pix is black  and labels is 1 
                    new_copy[i,j] = 0
                    #bellow if statemnt is not really needed
                    #but kept it here to show that im labeling different pieces
                # if labels[i][j] == 2:#if  curr pix is black and label is 2
                #     new_copy[i,j] = 100
                if labels[i][j] > 1 :
                    new_copy[i,j] =150
                else:
                    pass
        return new_copy
        
    def square(img):# gettign square around the circle 
        new_copy = img.copy()
        
        #new_label = []
        counter = 0
        total_x = 0
        total_y = 0
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                if img[i,j] == 0:
                    counter +=1

                    total_x += i
                    total_y += j
        average_x = total_x / counter
        average_y = total_y / counter
        center = [int(average_x),int(average_y)]

        smallest_i = -1
        biggest_i = -1
        smallest_j = -1
        biggest_j = -1     
        #following gets the   outter radius of the circle 
        for i in range(0, img.shape[0]):#x
                for j in range(0, img.shape[1]):#y
                    if img[i][j] == 0:# on;y in circle 
                        if smallest_i == -1:
                            smallest_i = i
                            biggest_i = i
                            smallest_j = j
                            biggest_j = j

                        elif smallest_i > i:
                            smallest_i = i

                        elif biggest_i < i:
                            biggest_i = i

                        elif smallest_j > j:
                            smallest_j = j
                        
                        elif biggest_j < j:
                            biggest_j = j
                     
                   
        top = biggest_j - average_y
        bottom = smallest_j - average_y
        left = smallest_i - average_x
        right = biggest_i - average_x
        #  get the 4 sides of the circle and get the average of them all and thats the outer pount 
        average_outer_radius = (top + abs(bottom) + abs(left) + right) /4 #this is the outter radius
    
        small_radius=0
        #to get inner start at the center and loop to any side until you hit black pixel thats inner radius 
        for y in range(center[1],len(img)):
            if img[center[0],y] != 0:
                small_radius +=1
            else:
                break

        for x in range(0, img.shape[0]):#x
            for y in range(0, img.shape[1]):#y
                #using equation to check for perfect circle 
                #(x - a)sqrt + (y = b)sqrt = r sqrt
                #so if on outer but not on inner radius 
                if ((x - center[0])**2) + ((y - center[1])**2  ) <= average_outer_radius **2 and not ((x - center[0])**2) + ((y - center[1])**2  ) <= small_radius **2:
                    new_copy[x,y] = 100
                else:
                    new_copy[x,y] = 0
        answer = True
        # circles are not perfect so need to add some allowance to them so im checking 
        #for next neighbour pixel if in the equation then i label s true 
        #i can check few neighbours since errors are bigger than just one pixel
        for x in range(0, img.shape[0]):#x
            for y in range(0, img.shape[1]):#y
                if img[x,y] !=0 and new_copy[x,y] == 100:
                    if img[x-1,y] != 0 and img[x+1,y] != 0 and img[x,y-1] != 0 and img[x,y+1] != 0:
                        if img[x-2,y] != 0 and img[x+2,y] != 0 and img[x,y-2] != 0 and img[x,y+2] != 0:
                            if img[x,y] != 0 and img[x,y] != 0 and img[x,y] != 0 and img[x,y+3] != 0:
                                answer = False                          
        print(answer)
        img[smallest_i,smallest_j:biggest_j]=0
        img[biggest_i,smallest_j:biggest_j]=0
            
        for y in range(smallest_i,biggest_i):
            img[y,smallest_j] = 0
            img[y,biggest_j] = 0
        return img

    hist = imhist(img) 
    img = threshold(img,max_x-50)#this makes everything either 0 or 255
    before = time.time()

    img = closing(img)
    img = painting(img)
    hist = imhist(img)
    plt.plot(hist)
    print("max x axis value is = ",max_x)
    img = square(img)
    after = time.time()
    print("Time taken to process hand coded thresholding: " + str(after-before))

    cv.imshow('thresholded image 1',img)
    cv.waitKey(0)
    cv.destroyAllWindows()