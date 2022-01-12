import numpy as np
import cv2
from PIL import Image
import io
import numpy as np
from game_controller import GameController

def convert_img(image):
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img =  cv2.Canny(processed_img, threshold1 = 200, threshold2=300)
    return processed_img


def process_image(image):
    img = Image.open(io.BytesIO(image))
    screen = np.asarray(img)
    new_screen = convert_img(screen)
    cv2.imshow('window', new_screen)
    cv2.waitKey(0)

gw = GameController()
gw.start_browser()
gw.startup_game()
process_image(gw.get_game_frame())