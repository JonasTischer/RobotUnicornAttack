from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.element_has_css_value import element_has_css_value
from selenium.webdriver.common.by import By


class GameController:

    driver = None
    game_canvas = None

    def __init__(self) -> None:
        self.driver = Chrome()

    def start_browser(self):
        url = "https://www.crazygames.com/game/robot-unicorn-attack"
        self.driver.get(url)

    def expand_shadow_element(self, element):
        # return a list of elements
        shadowRoot = self.driver.execute_script(
            'return arguments[0].shadowRoot.children', element)
        return shadowRoot

    def startup_game(self):
        # Agree to Cookies
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[3]/div/div[1]/div[2]/button[2]"))).click()

        # Switch to Game Frame
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "game-iframe")))

        # Locate Play Now Button
        play_now_button = self.driver.find_element(
            by=By.XPATH, value="//div[@class='jss74 jss75']")
        play_now_button.click()

        # Press anywhere to start game
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "game-container")))

        ruffle_player = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.TAG_NAME, "ruffle-player")))

        shadowRoot = self.expand_shadow_element(ruffle_player)

        game_canvas = WebDriverWait(shadowRoot[2], 10).until(
            element_has_css_value((By.TAG_NAME, "canvas"), "cursor", "pointer"))
        self.game_canvas = game_canvas
        print("Click Canvas")
        print(game_canvas.location)
        print(game_canvas.size)
        game_canvas.click()

    def shutdown_game(self):
        self.driver.quit()

    def get_game_frame(self):
        return self.game_canvas.screenshot_as_png
