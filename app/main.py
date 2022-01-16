from game_controller import GameController
from game_handler import GameHandler
from model import Model
import argparse

def playGame():
    game_controller = GameController()
    game_controller.start_browser()
    game_controller.startup_game()
    game_handler = GameHandler(game_controller)
    # game_handler.play_game()
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-m', '--mode', help='Train / Run', required=True)
    args = vars(parser.parse_args())
    game = Model(game_handler)
    game.playGame(args)
    
def main():
    playGame()

if __name__ == "__main__":
    main()
