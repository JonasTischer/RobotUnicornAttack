import imp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from io import BytesIO
import skimage as skimage
from skimage import transform, color, exposure, io
from skimage.transform import rotate
import numpy as np
from keras.initializers import normal, identity
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv2D, Convolution2D, MaxPooling2D
from tensorflow.keras.optimizers import SGD, Adam
import tensorflow as tf
import argparse
from collections import deque
import random
import json
import os
from skimage.util import img_as_uint
from game_handler import GameHandler
from game_controller import GameController
import time

ACTIONS = 3  # number of valid actions
GAMMA = 0.99  # decay rate of past observations
OBSERVATION = 800.  # timesteps to observe before training
EXPLORE = 2500.  # frames over which to anneal epsilon
FINAL_EPSILON = 0.0001  # final value of epsilon
INITIAL_EPSILON = 0.1  # starting value of epsilon
REPLAY_MEMORY = 25000  # number of previous transitions to remember
BATCH = 64  # size of minibatch
FRAME_PER_ACTION = 1
LEARNING_RATE = 0.0003

class Model():
    def __init__(self, game_handler: GameHandler):
        super().__init__()
        self.game_handler = game_handler

    def buildmodel(self):
        model = Sequential()

        model.add(Conv2D(32, (3, 3), padding='same',
                         input_shape=(487, 649, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(512, activation='relu'))
        model.add(Dense(3, activation='softmax'))
        model.compile(optimizer='adam', loss="mse", metrics=["accuracy"])
        return model

    def train(self, model, args):
        last_time = time.time()
        D = deque()
        frame = self.game_handler.state["frame"]
        stacked_frames = np.stack((frame, frame, frame), axis=2)
        stacked_frames = stacked_frames.reshape(
            1, stacked_frames.shape[0], stacked_frames.shape[1], stacked_frames.shape[2])
        
        if args['mode'] == 'Run':
            OBSERVE = 999999999  # We keep observe, never train
            epsilon = FINAL_EPSILON
            print("Now we load weight")
            model.load_weights("model.h5")
            model.compile(optimizer='adam', loss="mse", metrics=["accuracy"])
            print("Weight load successfully")
        else:  # We go to training mode
            OBSERVE = OBSERVATION
            epsilon = INITIAL_EPSILON
            if os.path.isfile('./model.h5'):
                model.load_weights("model.h5")
                model.compile(optimizer='adam', loss="mse",
                              metrics=["accuracy"])
                print("Weight load successfully")

        t = 0
        #self.game_handler.play_game()
        while(True):
            sleep(0.05)
            if self.game_handler.get_playing() == False:
                self.game_handler.restart()
                self.game_handler.get_game_state(t)
                continue
            loss = 0
            Q_sa = 0
            action_index = 0
            r_t = 0
            a_t = np.zeros([ACTIONS])
            if t % FRAME_PER_ACTION == 0:
                if random.random() <= epsilon:
                    print("----------Random Action----------")
                    action_index = random.randrange(ACTIONS)
                    a_t[action_index] = 1
                else:
                    # input a stack of 3 images, get the prediction
                    q = model.predict(stacked_frames)
                    print("q: ", q)
                    max_Q = np.argmax(q)
                    action_index = max_Q
                    a_t[max_Q] = 1

            #We reduce the epsilon gradually
            if epsilon > FINAL_EPSILON and t > OBSERVE:
                epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

            self.game_handler.take_action(action_index)
            self.game_handler.get_game_state(t)
            print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
            frame1 = self.game_handler.state["frame"]
            frame1 = frame1.reshape(1, frame1.shape[0], frame1.shape[1], 1)
            stacked_frames1 = np.append(
                frame1, stacked_frames[:, :, :, :2], axis=3)

            r_t = self.game_handler.get_reward()

            # store the transition in D
            D.append((stacked_frames, action_index, r_t,
                     stacked_frames1, not self.game_handler.get_playing()))
            if len(D) > REPLAY_MEMORY:
                D.popleft()

            #only train if done observing
            if t > OBSERVE:
                #sample a minibatch to train on
                minibatch = random.sample(D, BATCH)

                #Now we do the experience replay
                state_t, action_t, reward_t, state_t1, terminal = zip(
                    *minibatch)
                state_t = np.concatenate(state_t)
                state_t1 = np.concatenate(state_t1)
                targets = model.predict(state_t)
                Q_sa = model.predict(state_t1)
                targets[range(BATCH), action_t] = reward_t + \
                    GAMMA*np.max(Q_sa, axis=1)*np.invert(terminal)

                loss += model.train_on_batch(state_t, targets)[0]

            stacked_frames = stacked_frames1
            t = t+1

            #save progress every 1000 iterations
            if t % 1000 == 0:
                print("clearing memory..")
                os.system("sync; echo 1 >  /proc/sys/vm/drop_caches")
                print("Save model")
                model.save_weights("model.h5", overwrite=True)
                with open("model.json", "w") as outfile:
                    json.dump(model.to_json(), outfile)

            # print info
            state = ""
            if t <= OBSERVE:
                state = "observing"
            elif t > OBSERVE and t <= OBSERVE + EXPLORE:
                state = "exploring"
            else:
                state = "training"

            print("TIMESTEP", t, "/ STATE", state,
                  "/ EPSILON", epsilon, "/ ACTION", action_index, "/ REWARD", r_t,
                  "/ Q_MAX ", np.max(Q_sa), "/ Loss ", loss, "/ Score ", self.game_handler.get_score())

        print("Episode finished!")
        print("************************")

    def playGame(self, args):
        model = self.buildmodel()
        self.train(model, args)
