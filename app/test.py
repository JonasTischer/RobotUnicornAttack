import pytesseract
from PIL import Image
import cv2

# Simple image to string

#img = Image.open('test.png')

template_img = cv2.imread('./state-frames/two_life_left_cross.png')
cropped_template = template_img[0:40, 0:150]
#dimensions = img.shape
#cv2.imshow('cropped', cropped)
#cv2.waitKey(0)

img = cv2.imread('./state-frames/one_life_left_test.png')
cropped_image = img[0:40, 0:150]
res = cv2.matchTemplate(cropped_image, cropped_template, cv2.TM_CCORR_NORMED)
print(res)
#cv2.imshow('cropped', res)
#cv2.waitKey(0)
#print(pytesseract.image_to_string(img))

def draw_boxes_and_show(cv_image):
    cv2.rectangle(cv_image, (250, 10), (600, 60), (0, 0, 255), 2)
    cv2.imshow('window',cv_image)
    cv2.waitKey(0)
    return cv_image


#print(pytesseract.image_to_string(draw_boxes_and_show(img)))


