from game_controller import GameController
from utils.image_processor import get_score_from_image, get_state_from_image
import time


class GameHandler:

    game_states = ["Welcome_Screen", "In_Game", "Score_Board"]
    # action_space = { "Dash": "X",
    #                 "Jump": "Z",
    #                 "Nothing": ""}
    action_space = ["X", "Z", ""]

    def __init__(self, game_controller: GameController):
        self.game_controller = game_controller
        self.state = self.get_game_state(-1)

    def get_score(self):
        return self.state["score"]

    def get_game_state(self, time):
        unprocessed_frame = self.game_controller.get_game_frame()
        self.state = get_state_from_image(unprocessed_frame, time)
        return self.state

    def get_frame(self):
        return self.state["frame"]

    def restart(self):
        print("Not playing, press Z to restart")
        self.take_action(1)

    def get_reward(self):
        if self.get_playing() == True:
            return 1
        else:
            return -1

    def get_crashed(self):
        return self.state["is_crashed"]
    
    def get_playing(self):
        return self.state["is_playing"]
    
    def take_action(self, action):
        print("Action from handler")
        self.game_controller.input_action(self.action_space[action])
        
    def reset_game(self):
        pass
    
    def play_one_round(self):
        state = self.reset_game()
        done = False
        accumulated_reward = 0
        time_step = 0
        last_time = time.time()
        while not done:
            state = self.get_game_state(time_step)
            action = self.get_action(0)
            reward, done, info = self.take_action(action)
            accumulated_reward += reward
            time_step += 1
            print('Loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
        return accumulated_reward
    
    def play_game(self):
        self.game_controller.start_browser()
        self.game_controller.startup_game()
        
        game_state = self.get_game_state(-1)
        action = self.get_action(game_state)
        self.take_action(action)
        
        #self.play_one_round()