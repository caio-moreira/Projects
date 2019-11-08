import os
import numpy as np
import cv2
import pandas as pd
from PIL import Image as img


# "Global" variables, containing the paths of the most relevant directories
current_file_path = os.path.dirname(__file__)
images_path = os.path.join(current_file_path, "images")
test_data_path = os.path.join(current_file_path,"test_data")
train_data_path = os.path.join(current_file_path,"train_data")

def get_sub_image(coordinates, image):
    """ Function that cuts a given image using given coordinates.
  
    Keyword arguments: 
        coordinates -- coordinates of where to cut the image 
        image -- image to cut from. must be numpy array.

    Returns:
        sub_image -- cut from original image.
    """

    # Saving coordinates of the face inside the "root" image
    x, y, w, h = coordinates

    # Saving the numpy array of the face, using coordinates
    sub_image = image[y:y + h, x:x + w]

    return sub_image

def get_faces(image):
    """ Function that returns all the faces in a given image.

    This function selects every face detected in a given image and returns them in a list.
  
    Keyword arguments: 
        image -- image to select faces from. must be numpy array.
    """
    
    faces = []

    for index, face_coordinates in enumerate(cascade_classifier.detectMultiScale(image)):
        faces.append(get_sub_image(face_coordinates, image))

    return faces

def save_faces(cascade_classifier, img_filename):
    """ Function that saves all the faces in a given image.

    This function selects every face detected in a given image and saves it.
  
    Keyword arguments: 
        cascade_classifier -- the object of the cascade classifier
        img_filename -- name of the image.
    """
    
    # Opening the image and converting it to grayscale, then converting it to a numpy array
    image = img.open(os.path.join(images_path, img_filename)).convert('L')
    image_as_array = np.array(image, 'uint8')

    # Iterating through each face detected with detectMultiScale
    # detectMultiScale returns the coordinates of the faces inside the image
    for index, face in enumerate(get_faces(image_as_array)):
        # Creates the path that will receive the output images if it doesn't exist
        if not os.path.exists(test_data_path):
            os.makedirs(test_data_path)

        # Saves the face to the path
        # Naming pattern: rootImgName_index.jpg
        cv2.imwrite(os.path.join(
            test_data_path,
            '{}_{}.jpg'.format(img_filename.replace('.jpg', ''), index)),
            face
        )

if __name__ == "__main__":
    # Instantiates the cascadeClassifier from .xml file
    cascade_path = os.path.join(current_file_path, "haarcascade_frontalface_default.xml")
    cascade_classifier = cv2.CascadeClassifier(cascade_path)

    # Iterates through all the files in the images folder
    # this will populate the test_data folder
    for image_filename in os.listdir(images_path):
        # Saves each face in each image
        save_faces(cascade_classifier, image_filename)

    # Instantiates LBPH face recognizer
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Lists to store the faces detected from train data and respective labels
    train_faces = []
    labels = []

    # Iterates through each subject in train data
    # each one must have its own folder containing train data
    for subject in os.listdir(train_data_path):
        # Saves the path to current subject's train data
        subject_path = os.path.join(train_data_path, subject)

        # Goes through each photo of the subject in directory
        for image_name in os.listdir(subject_path):
            image = img.open(os.path.join(subject_path, image_name)).convert('L')
            image_as_array = np.array(image, 'uint8')

            # Using [0] because if there's only one face (the case here)
            # the get_faces() method will still return a one item list 
            face = get_faces(image_as_array)[0]

            train_faces.append(face)
            labels.append(int(subject))

    # Trains the recognizer using train data and labels, labels must be a numpy array
    face_recognizer.train(train_faces, np.array(labels))

    # Goes through each face detected in test path
    for face_filename in os.listdir(test_data_path):
        # Loads images as cv2 image object and saves its dimensions
        # 0 tells the imread method to open image in grayscale
        face = cv2.imread(os.path.join(test_data_path, face_filename), 0)
        height, width = face.shape
        
        # Other way of converting the image to grayscale
        # gray_scale = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        prediction = face_recognizer.predict(face)

        predicted_label = str(prediction[0])
        confidence = prediction[1]

        # Sets a name for the window that will be shown
        # Using both predicted and true labels for evaluation
        window_name = str('Predicted: ' + predicted_label + ' Actual: ' + face_filename)
        # Creates a window
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        # Moves the window to [100, 100] in the screen
        cv2.moveWindow(window_name, 100, 100)
        # Mantains window in its original proportions, avoiding distortions
        # Multiplying by 3 so that the name of the window is visible
        cv2.resizeWindow(window_name, height*3, width*3)
        # Shows the window with the face inside
        cv2.imshow(window_name, face)
        # Waits for any key to move on
        cv2.waitKey(0)
        # Kills the window, so that in the next iteration
        # another window can be opened without crowding the screen
        cv2.destroyAllWindows()