import os
import csv
import numpy as np
import cv2
from skimage import measure

# parameters for image comparison
# MSE stands for Mean Squared Error
max_mse = 0
min_ssim = 0.9

dataset_folder = 'dataset'
csv_file_name = 'duplicates.csv'

# rootdir = os.getcwd()   # get current working directory of a process
# path = os.path.join(rootdir, dataset_folder)
# print('path = ', path)

# get all files from dataset_folder
file_paths = []
for subdir, dirs, files in os.walk(dataset_folder):
    for file in files:
        # print(os.path.join(subdir, file))
        filepath = subdir + os.sep + file
        file_paths.append(filepath)
file_paths.sort()


with open(csv_file_name,'w') as newFile:
    newFileWriter = csv.writer(newFile)
    # newFileWriter.writerow(['name-to-keep','height 1', 'width 1', 
    # 'channels 1', 'name-to-delete', 'height 2', 'width 2', 'channels 2'])
    newFileWriter.writerow([
        'image-1','shape-1', 
        'image-2', 'shape-2',
        'mse', 'ssim'])
print('file initiated')

print('file_paths = ', file_paths)

for i, file in enumerate(file_paths):
    # print('%s of %s: processing %s' %(i + 1, len(file_paths), file))
    print('%s of %s: processing %s' %(i + 1, len(file_paths), file_paths[i]))
    # Open image
    img1 = cv2.imread(file)
    if img1 is None:
        print('--(!)Error: Failed reading image ', file)
        continue
    # get height, width and channels of img1
    h1, w1, ch1 = img1.shape
    # make image black'n'white
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    # compare current image with images that are further down the list 
    # as we have compared it with all previous images by this point
    j = i + 1
    while j < len(file_paths):
        img2 = cv2.imread(file_paths[j])
        if img2 is None:
            print('--(!)Error: Failed reading image ', file_paths[j])
            j += 1
            continue
        # get height, width and channels of img1
        h2, w2, ch2 = img2.shape
        # convert img2 to match resolution of img1 and make it black'n'white
        img2 = cv2.resize(img2, (w1, h1))
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # compute the mean squared error and structural similarity
        # index for the images
        m = measure.compare_mse(img1, img2)
        s = measure.compare_ssim(img1, img2)

        if m <= max_mse or s > min_ssim:
            print('      found similar image: %s' %(file_paths[j]))
            with open(csv_file_name,'a') as csv_file:
                fileWriter = csv.writer(csv_file)
                fileWriter.writerow([
                    file_paths[i], (h1, w1, ch1),
                    file_paths[j], (h2, w2, ch2),
                    m, s])
        j += 1