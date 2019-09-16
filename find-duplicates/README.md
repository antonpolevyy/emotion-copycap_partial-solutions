## Note

* find-duplicates.py        - creates duplicates.csv file with similar pictures
* view-delete-duplicates.py - display pairs from duplicates.csv and delete or skip manually
* delete-duplicates.py      - automatically deletes files from the list in duplicates.csv 

!!Note that find-duplicates.py will compare every next image faster and faster. Inside the main loop, it compares every image to all the other images, but skip those that has been compared before. 

First place all the images in the 'dataset' folder
Then run bash commands from curent folder
```
python find-duplicates.py
python delete-duplicates.py
```
or 
```
python find-duplicates.py
python view-delete-duplicates.py
```


# Pre-requisites

If don't have it or not shure execute in Terminal:
```
pip install tensorflow
pip install opencv-python
pip install skimage
```
# MSE and SSIM

MSE and SSIM are two of numerious ways to compare images

## MSE - Mean Squared Error
To count MSE for two pictures A and B:
Take the square of the difference between every pixel in A and the corresponding pixel in B, sum that up and divide it by the number of pixels

output range:
* 0                     - perfect similarity (all pixels where the same)
* hundreds and more     - the more pixels differ the more were added up to the sum

## SSIM - Structural Similarity Index
More complex method. It attempts to model the perceived change in the structural information of the image - smart sentense, right? ;)

output range:
* between -1 and 1, where 1 indicates perfect similarity


# About file paths

I'm using 'path' from 'os' libraries instead of simply specifying a string, because of the different path separation in Linux vs Windows systems 

Linux and macOS use 'folder/filename'
Windows uses 'folder\\filename' 

Therefor, to get file 'folder/filename' in this code next is done:
```
import os
path = os.path.join(folder, filename)
# or
path = folder + os.sep + filename
```
