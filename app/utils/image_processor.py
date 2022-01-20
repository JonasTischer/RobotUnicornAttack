import numpy as np
import cv2
from PIL import Image
import io
import numpy as np
from game_controller import GameController
from io import BytesIO
import pytesseract
import random


def get_processed_image(frame, count):
    img = Image.open(io.BytesIO(frame))
    screen = np.asarray(img)

    #img = cv2.imread(frame)
    #frame_img = skimage.color.rgb2gray(frame_img)
    img_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Blur the image for better edge detection
    #img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)

    # edge detection
    processed_img = cv2.Canny(img_gray, threshold1=85, threshold2=255)
    #processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
    #cv2.imwrite('./frames/frame-{}.png'.format(count), processed_img)
    return processed_img


def get_score_from_image(frame, count):
    #img = Image.open(io.BytesIO(frame))
    # nparr = np.frombuffer(frame, np.uint8)
    # img = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)

    # img = Image.open(io.BytesIO(frame))
    # screen = np.asarray(img)

    #img = cv2.imread(frame)
    #frame_img = skimage.color.rgb2gray(frame_img)
    # img_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Blur the image for better edge detection
    #img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)

    # edge detection
    # processed_img =  cv2.Canny(img_gray, threshold1 = 85, threshold2=255)

    cropped_image = frame[10:60, 250:600]
    score = pytesseract.image_to_string(cropped_image, config='--psm 6')
    #cv2.imwrite('./score-frames/frame-{}-{}.png'.format(count, score), cropped_image)
    return score


def get_state_from_image(frame, count):
    state = {}

    processed_img = get_processed_image(frame, count)

    state["score"] = get_score_from_image(processed_img, count)
    state["is_crashed"] = check_if_crashed(processed_img)
    state["is_playing"] = check_if_playing(processed_img, count)
    state["time"] = count
    state["frame"] = processed_img

    return state


def check_if_crashed(image):
    return random.random() < 0.1


def check_if_playing(image, count):
    template_img_one_life = cv2.imread('./state-frames/one_life_left.png')
    template_img_one_life = cv2.cvtColor(
        template_img_one_life, cv2.COLOR_BGR2GRAY)
    cropped_template_one_life = template_img_one_life[0:40, 0:150]
    template_img_two_life = cv2.imread('./state-frames/two_life_left.png')
    template_img_two_life = cv2.cvtColor(
        template_img_two_life, cv2.COLOR_BGR2GRAY)
    cropped_template_two_life = template_img_two_life[0:40, 0:150]
    template_img_three_life = cv2.imread('./state-frames/three_life_left.png')
    template_img_three_life = cv2.cvtColor(
        template_img_three_life, cv2.COLOR_BGR2GRAY)
    cropped_template_three_life = template_img_three_life[0:40, 0:150]
    cropped_image = image[0:40, 0:150]

    res = cv2.matchTemplate(
        cropped_image, cropped_template_three_life, cv2.TM_CCORR_NORMED)
    if res > 0.8:
        return True

    res = cv2.matchTemplate(
        cropped_image, cropped_template_two_life, cv2.TM_CCORR_NORMED)
    if res > 0.8:
        return True

    res = cv2.matchTemplate(
        cropped_image, cropped_template_one_life, cv2.TM_CCORR_NORMED)
    if res > 0.8:
        return True

    #cv2.imwrite('./not-playing-frames/frame-{}.png'.format(count,
    #                                              ), image)
    return False
