# Controls: 
# Esc or Q - close program 
# L - delete left file 
# R - delete Right file 
# any other key - next pair



import os
import csv
import numpy as np
import cv2

# dataset_folder = 'dataset'
csv_file_name = 'duplicates.csv'
# Note: rows of duplicates.csv made by find-duplicates.py has next structure
# | 'image-1' | 'shape-1' | 'image-2' | 'shape-2' | 'mse' | 'ssim' | 

# read file names from duplicates.csv
duplicates = []
with open(csv_file_name, 'r') as csvFile:
    print('file opened')
    csvReader = csv.DictReader(csvFile)
    for row in csvReader:
        duplicates.append(row)

# loop through pairs from duplicates
for duplicate in duplicates:
    print('img-1 = ', duplicate['image-1'])
    # Open image-1 and image-2
    img1 = cv2.imread(duplicate['image-1'])
    img2 = cv2.imread(duplicate['image-2'])

    # skip loop iteration if one of the images failed to load
    if img1 is None:
        print('---[ERROR]--- Failed to read image from file %s. Skipping iteration' %(duplicate['image-1']))
        continue
    if img2 is None:
        print('---[ERROR]--- Failed to read image from file %s. Skipping iteration' %(duplicate['image-2']))
        continue
    
    h1, w1, ch1 = img1.shape
    h2, w2, ch2 = img2.shape
    # resize images to height h
    h = 400
    ratio = h / h1
    w = int(w1 * ratio)
    img1 = cv2.resize(img1, (w, h))
    img2 = cv2.resize(img2, (w, h))
    # add text with image name and resolution
    text1 = '(' + str(w1) + ', ' + str(h1) + ')' + ': ' + duplicate['image-1']
    text2 = '(' + str(w1) + ', ' + str(h1) + ')' + ': ' + duplicate['image-2']
    startX = 0
    startY = 12
    txt_color = (0, 0, 255)
    cv2.putText(img1, text1, (startX, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, txt_color, 2)
    cv2.putText(img2, text2, (startX, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, txt_color, 2)
    # stack images horizontally (img1 to the left of img2)
    imgs = np.concatenate((img1, img2), axis=1)



    cv2.imshow('Controls: Esc - exit, L - delete Left, R - delete Right, Space - skip', imgs)
    key = cv2.waitKey(0)

    if key == ord("l"):
        try:
            os.remove(duplicate['image-1'])
        except OSError:
            print('---[ERROR]--- Failed to delete ', file)
            pass

    if key == ord("r"):
        try:
            os.remove(duplicate['image-2'])
        except OSError:
            print('---[ERROR]--- Failed to delete ', file)
            pass

    # if the `esc` or `q` key was pressed, break from the loop
    if key == 27 or key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()