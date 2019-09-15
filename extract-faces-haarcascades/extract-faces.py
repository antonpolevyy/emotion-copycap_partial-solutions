import numpy as np
import cv2
import os

# Paths to dataset and face detection model(s)
dataset_input_path = 'dataset_input'
dataset_output_path = 'dataset_output'

# resolution for cutted faces, 
# to keep all images in final dataset of same size
out_resolution = (350, 350)

# os.path.sep.join() used here instead of simply 'folder/filename' 
# because of different path separation in Linux vs Windows systems
# Linux uses 'folder/filename'
# Windows uses 'folder\\filename' 
haarcascade_paths = []
haarcascade_paths.append(os.path.join('OpenCV_FaceCascade', 'haarcascade_frontalface_default.xml'))
haarcascade_paths.append(os.path.join('OpenCV_FaceCascade', 'haarcascade_frontalface_alt2.xml'))
haarcascade_paths.append(os.path.join('OpenCV_FaceCascade', 'haarcascade_frontalface_alt.xml'))
haarcascade_paths.append(os.path.join('OpenCV_FaceCascade', 'haarcascade_frontalface_alt_tree.xml'))


################################################################################
# Function Definitions 
################################################################################

def extract_faces(emotion):
    # Get list of all images in 'emotion' folder
    path = os.path.sep.join([dataset_input_path, emotion])
    # get files in 'emotion' folder and sort them alphabetically
    dirpath, dirnames, filenames = next(os.walk(path))
    files = []
    for f in filenames:
        files.append(os.path.join(emotion, f))
    files.sort()

    # files_total = len(files)
    counter = 1
    for f in files:
        print('folder %s: %s of %s' %(emotion, counter, len(files)))
        counter += 1
        # Open image
        frame = cv2.imread(os.path.join(dataset_input_path, f))
        if frame is None:
            print('--(!)Error: Failed reading image ', f)
            continue

        # Convert image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Go through face detectors and stop at first success
        for detector in face_detectors:
            datected_faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
            if len(datected_faces) > 0:
                # Cut and save face
                for (x, y, w, h) in datected_faces:
                    # Cut the frame to size
                    face = frame[y : y+h, x : x+w]
                    # save face into separate files
                    try:
                        # Make picture black'n'white
                        bwFace = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                        # Resize so all images have the same resolution
                        out_image = cv2.resize(bwFace, out_resolution)
                        out_path = os.path.join(dataset_output_path, f)

                        # if such filename exists add "_" at the end
                        while (os.path.isfile(out_path)):
                            path_parts = os.path.splitext(out_path)
                            out_path = os.path.sep.join(path_parts[:-1]) + '_' + path_parts[-1]
                        
                        # save new file
                        cv2.imwrite(out_path, out_image)
                    except:
                        print('--(!)Error: Failed saving image ', out_path)
                        pass #If error, pass file
                # stop looping through detectors if operation succeeded
                break


################################################################################
# Program Execution 
################################################################################

# Copy folder names from dataset_input to assign categories ('happy', 'sad', 'neutral', etc)
dirpath, dirnames, filenames = next(os.walk(dataset_input_path))
categories = dirnames

# Create folders in dataset_output if such folders are not there
# cv2.imwrite() won't be able to save file in non existing folder
for categorie in categories:
    dir_path = os.path.join(dataset_output_path, categorie)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

# Load Haarcascades for face detection 
print("[INFO] loading face detectors...")
face_detectors = []
for path in haarcascade_paths:
    detector = cv2.CascadeClassifier(path)
    face_detectors.append(detector)

for emotion in categories:
    extract_faces(emotion)