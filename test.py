import os
import cv2 as cv

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

        full_path = test_root_path + "/" + file_name

        img = cv.imread(full_path)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        test_list.append(img_gray)
    
    return test_list


img = cv.imread("dataset/test/1.jpg")

print(img[0][0])
