import os
import cv2 as cv
import numpy as np

def get_path_list(root_path):
    '''
        To get a list of path directories from root path

        Parameters
        ----------
        root_path : str
            Location of root directory

        Returns
        -------
        list
            List containing the names of the sub-directories in the
            root directory
    '''
    sub_directory_names = []

    for folder_name in os.listdir(root_path):

        sub_directory_names.append(folder_name)

    return sub_directory_names


def get_class_id(root_path, train_names):
    '''
        To get a list of train images and a list of image classes id

        Parameters
        ----------
        root_path : str
            Location of images root directory
        train_names : list
            List containing the names of the train sub-directories

        Returns
        -------
        list
            List containing all image in the train directories
        list
            List containing all image classes id
    '''
    train_image_list = []
    class_id_list = []

    for idx, _ in enumerate(os.listdir(root_path)):

        sub_directory_path = root_path + "/" + train_names[idx]

        for file_name in os.listdir(sub_directory_path):

            image_full_path = sub_directory_path + "/" + file_name

            img = cv.imread(image_full_path)

            train_image_list.append(img)
            class_id_list.append(idx)
    
    return train_image_list, class_id_list



def detect_faces_and_filter(image_list, image_classes_list=None):
    '''
        To detect a face from given image list and filter it if the face on
        the given image is less than one

        Parameters
        ----------
        image_list : list
            List containing all loaded images
        image_classes_list : list, optional
            List containing all image classes id

        Returns
        -------
        list
            List containing all filtered and cropped face images in grayscale
        list
            List containing all filtered faces location saved in rectangle
        list
            List containing all filtered image classes id
    '''
    face_cascade = cv.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")

    filtered_cropped_images_list = []
    rects_list = []
    filtered_images_class_list = []

    for idx, image in enumerate(image_list):

        img_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        detected_face = face_cascade.detectMultiScale(img_gray, scaleFactor = 1.2, minNeighbors = 5)

        if len(detected_face) < 1:

            # filter
            continue
        
        for face_rect in detected_face:

            x, y, height, width = face_rect

            cropped_img_face = img_gray[y:y + height, x:x + width]

            filtered_cropped_images_list.append(cropped_img_face)
            rects_list.append(face_rect)

            if image_classes_list is not None:

                filtered_images_class_list.append(image_classes_list[idx])

    return filtered_cropped_images_list, rects_list, filtered_images_class_list



def train(train_face_grays, image_classes_list):
    '''
        To create and train face recognizer object

        Parameters
        ----------
        train_face_grays : list
            List containing all filtered and cropped face images in grayscale
        image_classes_list : list
            List containing all filtered image classes id

        Returns
        -------
        object
            Recognizer object after being trained with cropped face images
    '''
    face_recognizer = cv.face.LBPHFaceRecognizer_create()
    face_recognizer.train(train_face_grays, np.array(image_classes_list))

    return face_recognizer

def get_test_images_data(test_root_path):
    '''
        To load a list of test images from given path list

        Parameters
        ----------
        test_root_path : str
            Location of images root directory

        Returns
        -------
        list
            List containing all loaded gray test images
    '''
    test_list = [] 

    for file_name in os.listdir(test_root_path):

        # full path untuk setiap image test
        full_path = test_root_path + "/" + file_name

        # baca image
        img = cv.imread(full_path)

        # masukkan ke dalam list
        test_list.append(img)
    
    return test_list

def predict(recognizer, test_faces_gray):
    '''
        To predict the test image with the recognizer

        Parameters
        ----------
        recognizer : object
            Recognizer object after being trained with cropped face images
        train_face_grays : list
            List containing all filtered and cropped face images in grayscale

        Returns
        -------
        list
            List containing all prediction results from given test faces
    '''
    predict_result_list = []

    for cropped_img_test in test_faces_gray:

        result, _ = recognizer.predict(cropped_img_test)

        predict_result_list.append(result)

    return predict_result_list


def draw_prediction_results(predict_results, test_image_list, test_faces_rects, train_names):
    '''
        To draw prediction results on the given test images and acceptance status

        Parameters
        ----------
        predict_results : list
            List containing all prediction results from given test faces
        test_image_list : list
            List containing all loaded test images
        test_faces_rects : list
            List containing all filtered faces location saved in rectangle
        train_names : list
            List containing the names of the train sub-directories

        Returns
        -------
        list
            List containing all test images after being drawn with
            final result
    '''
    for idx in range(len(predict_results)):

        color = (0, 0, 0)
        text = ""

        image_label = train_names[predict_results[idx]]
        image_rect = test_faces_rects[idx]

        x, y, height, width = image_rect

        # Cek apakah image label agent atau bukan
        if "Agent" in image_label:
            
            # Jika agent maka color warna hijau (BGR)
            color = (0, 255, 0)
            text = image_label
        else:

            # Jika bukan agent maka color warna merah (BGR)
            color = (0, 0, 255)
            text = image_label + " (Fake)"

        cv.rectangle(test_image_list[idx], (x, y), (x + width, y + height), color, 2)
        cv.putText(test_image_list[idx], text, (x, y - 10), cv.FONT_HERSHEY_PLAIN, 3, color, 2)

    return test_image_list

def combine_and_show_result(image_list):
    '''
        To show the final image that already combine into one image

        Parameters
        ----------
        image_list : nparray
            Array containing image data
    '''
    resized_image_list = []

    for image in image_list:

        resized_image = cv.resize(image, (250, 250), interpolation = cv.INTER_AREA)
        resized_image_list.append(resized_image)

    first_col = np.vstack((resized_image_list[0], resized_image_list[3]))
    second_col = np.vstack((resized_image_list[1], resized_image_list[4]))
    third_col = np.vstack((resized_image_list[2], resized_image_list[5]))

    combined_cols = np.hstack((first_col, second_col, third_col))

    cv.imshow("Result", combined_cols)
    cv.waitKey(0)
    

'''
You may modify the code below if it's marked between

-------------------
Modifiable
-------------------

and

-------------------
End of modifiable
-------------------
'''
if __name__ == '__main__':
    
    '''
        Please modify train_root_path value according to the location of
        your data train root directory

        -------------------
        Modifiable
        -------------------
    '''
    train_root_path = 'dataset/train'
    '''
        -------------------
        End of modifiable
        -------------------
    '''

    train_names = get_path_list(train_root_path)
    train_image_list, image_classes_list = get_class_id(train_root_path, train_names)
    train_face_grays, _, filtered_classes_list = detect_faces_and_filter(train_image_list, image_classes_list)
    recognizer = train(train_face_grays, filtered_classes_list)
    '''
        Please modify train_root_path value according to the location of
        your data train root directory

        -------------------
        Modifiable
        -------------------
    '''
    test_root_path = 'dataset/test'
    '''
        -------------------
        End of modifiable
        -------------------
    '''
    
    test_image_list = get_test_images_data(test_root_path)
    test_faces_gray, test_faces_rects, _ = detect_faces_and_filter(test_image_list)
    predict_results = predict(recognizer, test_faces_gray)
    predicted_test_image_list = draw_prediction_results(predict_results, test_image_list, test_faces_rects, train_names)

    combine_and_show_result(predicted_test_image_list)