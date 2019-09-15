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
protoPath = os.path.sep.join(["face_detection_model", "deploy.prototxt"])
modelPath = os.path.sep.join(["face_detection_model",
	"res10_300x300_ssd_iter_140000.caffemodel"])

# minimal confidence. Parameter used by face detection 
minConfidence = 0.5



################################################################################
# Function Definitions 
################################################################################

# ----------- Extract Faces from image -------------------------
def extract_faces(emotion):
    # Get list of all images in 'emotion' folder
    path = os.path.sep.join([dataset_input_path, emotion])
    # get files in 'emotion' folder and sort them alphabetically
    dirpath, dirnames, filenames = next(os.walk(path))
    files = []
    for f in filenames:
        files.append(os.path.join(emotion, f))
    files.sort()

    counter = 1
    for f in files:
        print('folder %s: %s of %s' %(emotion, counter, len(files)))
        counter += 1
        # Open image
        frame = cv2.imread(os.path.join(dataset_input_path, f))
        if frame is None:
            print('--(!)Error: Failed reading image ', f)
            continue

        # a list of detected faces 
        detectedFaces = []

        # grab the image dimensions
        (h, w) = frame.shape[:2]

        # construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)
    
        # apply OpenCV's deep learning-based face detector to localize
        # faces in the input image
        detector.setInput(imageBlob)
        detections = detector.forward()

        # find index of detection with the the highest confidence
        confidences = []
        for i in range(0,detections.shape[2]):
            confidences.append(detections[0, 0, i, 2])
        index = np.argmax(confidences)

        # skip this file if the strongest detection is weaker than our minConfidence
        if confidences[index] < minConfidence: continue

        # compute the (x, y)-coordinates of the bounding box for the face
        box = detections[0, 0, index, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        # extract the face ROI
        face = frame[startY:endY, startX:endX]
        (fH, fW) = face.shape[:2]

        # ensure the face width and height are sufficiently large
        if fW < 20 or fH < 20:
            continue

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


################################################################################
# Program Execution 
################################################################################

# Copy folder names from dataset_input to assign categories ('happy', 'sad', 'neutral', etc)
dirpath, dirnames, filenames = next(os.walk(dataset_input_path))
categories = dirnames
print('categories = ', categories)

# Create folders in dataset_output if such folders are not there
# cv2.imwrite() won't be able to save file in non existing folder
for categorie in categories:
    dir_path = os.path.join(dataset_output_path, categorie)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

# Load our serialized face detector from disk
print("[INFO] loading face detector...")
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# Detect faces from dataset_input and extract them to dataset_output
for emotion in categories:
    extract_faces(emotion)
