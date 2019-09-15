## Note

This pre-trained caffee model may detect irrelative stuff as a face too
Thus use:

- 'extract-one-face-per-picture.py', if you know that all pictures have only one face that you need
```
python extract-one-face-per-picture.py
```

- 'extract-faces.py', but play with 'minConfidence' coefficient 
```
python extract-faces.py
```

# Pre-requisites

Make sure you have Tensorflow and OpenCV-Contrib

If don't have it or not shure execute in Terminal:
```
pip install tensorflow
pip install opencv-contrib-python
```

# Face detection with OpenCV and it's Caffe model 

The common way to detect faces with OpenCV is to use Haarcascades, but much quicker way is to use pre-trained deep learning Caffe model "res10_300x300_ssd_iter_140000.caffemodel"

You can read about this in "how_to_train_face_detector.txt" file from the official OpenCV repo under the face_detector folder of dnn module
[opencv/samples/dnn/face_detector](https://github.com/opencv/opencv/tree/master/samples/dnn/face_detector)

## Face detection Caffe model
There are copies of the propper files in face_detection_model folder

 * The .prototxt file(s) which define the model architecture (i.e., the layers themselves)
 * The .caffemodel file which contains the weights for the actual layers


# About file paths

I'm using 'path' from 'os' libraries instead of simply specifying a string, because of the different path separation in Linux vs Windows systems 

Linux and macOS use 'folder/filename'
Windows uses 'folder\\filename' 

Therefor, to get file 'folder/filename' in this code next is done:
```
import os
os.path.join(folder, filename)
```
