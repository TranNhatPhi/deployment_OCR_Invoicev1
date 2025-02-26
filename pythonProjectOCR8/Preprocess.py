# Preprocess.py

import cv2
import numpy as np
import math



# Các giá trị trong tiền xử lí Preprocess  ######################################################################
GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9

###################################################################################################

def preprocessing(image):
    img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    height, width = img_yuv.shape[:2]
    if height < 1000 and width < 1000:
        img_yuv = cv2.resize(img_yuv, (width * 2, height * 2))
    return img_yuv

def preprocess(imgOriginal):
    imgGrayscale = extractValue(imgOriginal)

    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)

    height, width = imgGrayscale.shape

    imgBlurred = np.zeros((height, width, 1), np.uint8)
#   Giảm nhiễu bằng cách làm mịn hình ảnh có thể giúp OCR phát hiện văn bản chính xác hơn:
    imgBlurred = cv2.GaussianBlur(
        imgMaxContrastGrayscale, GAUSSIAN_SMOOTH_FILTER_SIZE,0)

#Thresholding giúp tách biệt rõ ràng các vùng chứa văn bản và phông nền:
    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)
    # Nếu cần, tăng kích thước ảnh
    height, width = imgThresh.shape[:2]
    if height < 1000 and width < 1000:
        imgGrayscale = cv2.resize(imgThresh, (width * 2, height * 2))
        imgThresh = cv2.resize(imgThresh, (width * 2, height * 2))
    return imgGrayscale, imgThresh
# end function

###################################################################################################


def extractValue(imgOriginal):
    height, width, numChannels = imgOriginal.shape

    imgHSV = np.zeros((height, width, 3), np.uint8)

    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

    imgHue, imgSaturation, imgValue = cv2.split(imgHSV)

    return imgValue
# end function

###################################################################################################


def maximizeContrast(imgGrayscale):

    height, width = imgGrayscale.shape

    imgTopHat = np.zeros((height, width, 1), np.uint8)
    imgBlackHat = np.zeros((height, width, 1), np.uint8)

    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    imgTopHat = cv2.morphologyEx(
        imgGrayscale, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(
        imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)
    imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(
        imgGrayscalePlusTopHat, imgBlackHat)

    return imgGrayscalePlusTopHatMinusBlackHat
################################################################################################
# end function