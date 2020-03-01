import cv2 as cv
import numpy as np
import time
import matplotlib.pyplot as plt

#read in an image into memory
for folderout in range(6,7):
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
                                 if  x != 0 and y != 0 and i + x >= 0 and i+ x < img.shape[0] and j + y >= 0 and j + y < img.shape[1] and  img[i+x][j+y]==255:
                                    if i + x >= 0 and i+ x < img.shape[0] and j + y >= 0 and j + y < img.shape[1] and  img[i+x][j+y]==255:
                                        new_copy[i + x][j + y] =0
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

    def labeling(img):
        li = [[ 0 for i in range(0, img.shape[0])] for j in range(0, img.shape[1])]
        counter = 1
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                if img[i,j] == 0 and li[i][j] == 0:#if  curr pix is black
                    li[i][j] = counter
                    queue = []
                    queue.append([i,j])#added curr pixel to the queue
                    #
                    while len(queue)>0:
                        pixel = queue.pop(0)
                        #print(img[pixel[0] -1,pixel[1]])
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
                    counter +=1
            	        ## pushed here 
        return li

    def painting (img):
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

    def center_point(img):
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
        


        # img[int(average_x),int(average_y)] = 0
        # img[int(average_x - 1 ),int(average_y )] = 0
        # img[int(average_x + 1 ),int(average_y)] = 0
        # img[int(average_x - 1 ),int(average_y - 1 )] = 0
        # img[int(average_x + 1 ),int(average_y + 1)] = 0
        # img[int(average_x ),int(average_y - 1 )] = 0
        # img[int(average_x),int(average_y + 1)] = 0

        # img[int(average_x - 2 ),int(average_y )] = 0
        # img[int(average_x + 2 ),int(average_y)] = 0
        # img[int(average_x - 2 ),int(average_y - 2 )] = 0
        # img[int(average_x + 2 ),int(average_y + 2)] = 0
        # img[int(average_x ),int(average_y - 2 )] = 0
        # img[int(average_x),int(average_y + 2)] = 0

        return img
        
    def square(img):
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
        for i in range(0, img.shape[0]):#x
                for j in range(0, img.shape[1]):#y
                    if img[i][j] == 0:
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
        average_outer_radius = (top + abs(bottom) + abs(left) + right) /4 #this is the outter radius
        #nneed to do inner radius 
        #go from center point up and if you hit black pixel then your on radius
        # print(center[0], center[1]) this gives me the center point of the circle
        # img[center[0],center[1]] = 0
        #(x -a )sqrt + (y - b)sqrt = r sqrt
        #a and b = center point
        # new_label = [[ 0 for i in range(0, img.shape[0])] for j in range(0, img.shape[1])]
        # labels = labeling(img)## list of labels from labeling
                     
        # #print(labels)
        # if new_label == labels:#compare of labeling list is same as new lables
        #     print("TRUE")
        # else:
        #     print("FALSE")
        small_radius=0
        for y in range(center[1],len(img)):
            if img[center[0],y] != 0:
                small_radius +=1
            else:
                break
        #print(small_radius,"...." ,average_outer_radius)
        # distance = average_outer_radius - small_radius
        # print(distance)

        

        #print(small_radius)
        for x in range(0, img.shape[0]):#x
            for y in range(0, img.shape[1]):#y
                if ((x - center[0])**2) + ((y - center[1])**2  ) <= average_outer_radius **2 and not ((x - center[0])**2) + ((y - center[1])**2  ) <= small_radius **2:
                    
                    new_copy[x,y] = 100
                    # new_label[int(x)][int(y)] = 1#if in the range of radius change to 1
                else:
                    new_copy[x,y] = 0
                    #new_label[int(x)][int(y)] = 0#if outside change to 0   
        answer = True
        for x in range(0, img.shape[0]):#x
            for y in range(0, img.shape[1]):#y
                for al in range(1,6):
                    if img[x,y] !=0 and new_copy[x,y] == 100:
                        if img[x-al,y] != 0 and img[x+al,y] != 0 and img[x,y-al] != 0 and img[x,y+al] != 0:
                            answer = False
                       
        print(answer)

        

                    
            


        # print(top)
        # print(abs(bottom))
        # print(abs(left))
        # print(right)
        # print(average_radius)
        
        #print("top_radius is ",img[center,top_radius])                 
        #for x in range(smallest_j,biggest_j):
        #    img[smallest_i,x] = 0
        #    img[biggest_i,x ] = 0
        
        img[smallest_i,smallest_j:biggest_j]=0
        img[biggest_i,smallest_j:biggest_j]=0
            
        for y in range(smallest_i,biggest_i):
            img[y,smallest_j] = 0
            img[y,biggest_j] = 0

        return img

    #def checker(img):
    #(x -a )sqrt + (y - b)sqrt = r sqrt
    #a and b = center point

    hist = imhist(img) 
    img = threshold(img,max_x-50)#this makes everything either 0 or 255

    img = closing(img)
    #labels = labeling(img)
    img = painting(img)

    hist = imhist(img)
    plt.plot(hist)
    #plt.show()
    print("max x axis value is = ",max_x)
    img = center_point(img)
    img = square(img)
    cv.imshow('thresholded image 1',img)
    cv.waitKey(0)
    cv.destroyAllWindows()
  