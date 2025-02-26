# Preprocess.py

import cv2
import numpy as np
import math

# Các giá trị trong tiền xử lí Preprocess ######################################################################
GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9
BILATERAL_FILTER_DIAMETER = 9  # Đường kính của bộ lọc bilateral
BILATERAL_FILTER_SIGMA_COLOR = 75
BILATERAL_FILTER_SIGMA_SPACE = 75


###################################################################################################



def preprocess(imgOriginal):
    imgGrayscale = extractValue(imgOriginal)

    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)

    # Giảm nhiễu bằng bộ lọc bilateral để giữ biên sắc nét
    imgDenoised = cv2.bilateralFilter(imgMaxContrastGrayscale,
                                      BILATERAL_FILTER_DIAMETER,
                                      BILATERAL_FILTER_SIGMA_COLOR,
                                      BILATERAL_FILTER_SIGMA_SPACE)

    # Tăng cường độ nét của ảnh sau khi giảm nhiễu bằng bộ lọc bilateral
    imgSharpened = sharpen_image(imgDenoised)

    # Thresholding để tạo ảnh đen trắng rõ nét
    imgThresh = cv2.adaptiveThreshold(imgSharpened, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)

    # Nếu cần, tăng kích thước ảnh
    height, width = imgThresh.shape[:2]
    if height < 1000 and width < 1000:
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


def sharpen_image(img):
    # Kernel tăng cường độ nét
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    imgSharpened = cv2.filter2D(img, -1, kernel)
    return imgSharpened
# end function
