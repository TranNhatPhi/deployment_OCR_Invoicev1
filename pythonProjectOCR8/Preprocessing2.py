import cv2
import numpy as np

# Các giá trị trong tiền xử lí Preprocess ######################################################################
GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9
BILATERAL_FILTER_DIAMETER = 7  # Giảm kích thước bộ lọc để tăng tốc độ xử lý
BILATERAL_FILTER_SIGMA_COLOR = 50
BILATERAL_FILTER_SIGMA_SPACE = 50

###################################################################################################


def preprocess(imgOriginal):
    # Giảm kích thước ảnh nếu ảnh quá lớn để tăng tốc độ xử lý
    height, width = imgOriginal.shape[:2]
    if height > 1500 or width > 1500:
        imgOriginal = cv2.resize(imgOriginal, (width // 2, height // 2))

    imgGrayscale = extractValue(imgOriginal)

    # Tăng cường độ tương phản bằng CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    imgContrastEnhanced = clahe.apply(imgGrayscale)

    # Giảm nhiễu bằng bộ lọc bilateral để giữ biên sắc nét
    imgDenoised = cv2.bilateralFilter(imgContrastEnhanced,
                                      BILATERAL_FILTER_DIAMETER,
                                      BILATERAL_FILTER_SIGMA_COLOR,
                                      BILATERAL_FILTER_SIGMA_SPACE)

    # Tăng cường độ nét của ảnh sau khi giảm nhiễu bằng bộ lọc bilateral
    imgSharpened = sharpen_image(imgDenoised)

    # Thresholding để tạo ảnh đen trắng rõ nét
    imgThresh = cv2.adaptiveThreshold(imgSharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)

    # Nếu ảnh đầu ra nhỏ, tăng kích thước lên để dễ nhìn hơn
    height, width = imgThresh.shape[:2]
    if height < 1000 and width < 1000:
        imgThresh = cv2.resize(imgThresh, (width * 2, height * 2))
    return imgGrayscale, imgThresh

###################################################################################################


def extractValue(imgOriginal):
    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
    _, _, imgValue = cv2.split(imgHSV)
    return imgValue

###################################################################################################


def maximizeContrast(imgGrayscale):
    # Thay thế bởi CLAHE ở hàm preprocess, do đó không cần tối ưu thêm ở đây.
    pass

################################################################################################


def sharpen_image(img):
    # Kernel tăng cường độ nét được tối ưu để làm rõ văn bản trong ảnh
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    imgSharpened = cv2.filter2D(img, -1, kernel)
    return imgSharpened
# end function
