### Pre-requisites
```
pip install tensorflow
pip install opencv-python
```

## Note

- place pictures in 'dataset_input'
- execute command in Terminal 
```
python extract-faces.py
```

You better check the final result because many face detectors may recognise random stuff as a face too

# Haarcascades classifiers 
Haar Feature-based Cascade Classifiers are standard face, eyes and object detectors of OpenCV

You can read about it [here](https://docs.opencv.org/4.1.1/db/d28/tutorial_cascade_classifier.html)


# About file paths

I'm using 'path' from 'os' libraries instead of simply specifying a string, because of the different path separation in Linux vs Windows systems 

Linux and macOS use 'folder/filename'
Windows uses 'folder\\filename' 

Therefor, to get file 'folder/filename' in this code next is done:
```
import os
os.path.join(folder, filename)
```
