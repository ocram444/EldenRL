import os
import cv2
import gym
import time
import numpy as np
from gym import spaces
import mss
from EldenReward import EldenReward
import pydirectinput
import pytesseract                          #π This is used to read the text on the screen
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #πpath to pytesseract. We need it for image to string conversion

from walkToBoss import walk_to_boss         #π This is the function that walks from the grace to the boss. These are hard coded for every boss and need to be changed if you want to fight a different boss.

print("EldenEnv.py #0")


#π To do:
#π 0. 
#π 1. We need to be able to set our vigor stat somewhere. And the hp bar detection needs to be based on that. (in EldenReward)
    #π 1.1 Implement the vigor-hp csv file and make sure it works with the hp bar detection (how much hp the player has based on his vigor (how long the ho bar is))   (in EldenReward)
#π 2 Finally fix the health bar reading. Computer vision is weird... (in EldenReward)
#π 3. Tensorboard visualization (in train.py)


#π¦ OK here is what you need to do to run this:
#π¦ 0. Import what you need (keep in mind that you need to install python 3.9 and select it as the python interpreter. And some other stuff that is not just a simple pip install...)
#π¦ 1. Pick Mage starting class and create a new character. Equip left hand staff, right hand sword, only one spell, and only the healing flasks.
#π¦ 2. Start the game and load the character (and walk to a fog gate of the boss you want to fight)
#π¦ 3. Put the game in the top left corner of the screen and make it windowed 1920x1080 (its not to the very left of the screen. There is a small gap. You can render the screenshot to make sure its positioned correctly)
#π¦ 4. Run train.py 
#π¦ 5. The training will start in the reset function...
    #π¦ 5.1 The reset function looks for a loading screen and resets the game by walking back to the boss. (It will also end after 20seconds of not seeing a loading screen)
    #π¦ 5.2 When the reset function is done, the agent will take over and start taking actions
    #π¦ 5.3 The step function will repeat and take actions until it is determined to be done (the agent dies, the boss dies, or the fight takes more than 10minutes)
#π¦ 6 train.py will then save the model and start the next episode (the next reset)


#π Setting up some constants
N_CHANNELS = 3                                #π€· Something about the image format that is fed into the agents obserevation
IMG_WIDTH = 1920                              #π The width and height of the screenshot (game is 1920x1080)
IMG_HEIGHT = 1080                             
MODEL_WIDTH = int(800 / 2)                    #π The width and height of the screenshot that is fed into the model (the model dosnt need the full sized screenshot)
MODEL_HEIGHT = int(450 / 2)


DISCRETE_ACTIONS = {'release_wasd': 'release_wasd', #π All the action the agent can take (just a list to count them. This isnt used anywhere)
                    'w': 'run_forwards',                
                    's': 'run_backwards',
                    'a': 'run_left',
                    'd': 'run_right',
                    'shift': 'dodge',
                    'u': 'attack',
                    'i': 'strong_attack',
                    'o': 'magic',
                    'e': 'use_item'}

N_DISCRETE_ACTIONS = len(DISCRETE_ACTIONS)    #π The number of actions the agent can take  (This is actually used to define the action space) (9 actions)
NUM_ACTION_HISTORY = 10                       #π 10 previous actions are stored in the observation


#π Function to create an array of previous actions
#Just... its not a normal array. Its a one hot encoded array.
# This means that if we take action 2 it will look like this: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
#then we store 10 (NUM_ACTION_HISTORY) of these arrays in a list and return that list
#We do this so stablebaselines3 can use the previous actions as part of the observation
#I didnt know this data structure before. Its pretty cool.
def oneHotPrevActions(actions):
    oneHot = np.zeros(shape=(NUM_ACTION_HISTORY, N_DISCRETE_ACTIONS, 1))
    for i in range(NUM_ACTION_HISTORY):
        if len(actions) >= (i + 1):
            oneHot[i][actions[-(i + 1)]][0] = 1
    #print(oneHot)
    return oneHot 


#π Just for debugging purposes. It renders a cv2 image. Use it to make sure any screenshots are correct.
def render_frame(frame):                
    cv2.imshow('debug-render', frame)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()

        
#π The is the actual environment.
class EldenEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    #π The constructor of the class. This is where we initialize the environment.
    def __init__(self):
        super(EldenEnv, self).__init__()                        #π something about initializing the class correctly. I dont know but its required.
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS) #π action space that the agent can take. (0-9) (this is used in train.py)

        spaces_dict = {                                         #π observation space that the agent can see. (img, prev_actions, state)
            #π The agent can see the image of the game.
            'img': spaces.Box(low=0, high=255, shape=(MODEL_HEIGHT, MODEL_WIDTH, N_CHANNELS), dtype=np.uint8),
            #π The agent knows the last actions that it took. (true/false for each action) (see oneHotPrevActions)
            'prev_actions': spaces.Box(low=0, high=1, shape=(NUM_ACTION_HISTORY, N_DISCRETE_ACTIONS, 1), dtype=np.uint8),
            #π The agent knows the current state of the game. (health, stamina of player, *maybe more later)
            'state': spaces.Box(low=0, high=1, shape=(2,), dtype=np.float32),
        }
        self.observation_space = gym.spaces.Dict(spaces_dict)  #π Defining the observation space for gym. (this is used in train.py)
        
        #π Class variables
        self.reward = 0                         #π Current reward
        self.rewardGen = EldenReward()          #π Setting up the reward generator class (see EldenReward.py)
        self.death = False                      #π If the agent died
        self.t_start = time.time()              #π Time when the game started
        self.done = False                       #π If the game is done
        self.iteration = 0                      #π Current iteration (number of steps taken in this fight)
        self.first_step = False                 #π If this is the first step (is set to true in reset)
        #self.locked_on = False                 #π Log on needs to be hardcoded for now. (in walkToBoss.py)
        self.max_reward = None                  #π The maximum reward that the agent has gotten
        self.reward_history = []                #π array of the rewards to calculate the average reward of fight            
        self.sct = mss.mss()                    #π initializing CV2 and MSS (used to take screenshots)
        #self.boss_hp_end_history = []          #π array of the boss hp at the end of each run (not implemented)
        self.action_history = []                #π array of the actions that the agent took. (see oneHotPrevActions and the observation space)
        self.time_since_heal = time.time()      #π time since the last heal
        

    #π Grabbing the screenshot of the game
    def grab_screen_shot(self):
        for num, monitor in enumerate(self.sct.monitors[1:], 1):
            sct_img = self.sct.grab(monitor)    # Get get screenshot of whole screen
            frame = cv2.cvtColor(np.asarray(sct_img), cv2.COLOR_BGRA2RGB)
            frame = frame[46:IMG_HEIGHT + 46, 12:IMG_WIDTH + 12]    #cut the frame to the size of the game
            #render_frame(frame)    #π render the frame for debugging
            #print('π· screenshot grabbed')
            return frame
    
    #π Taking an action in the game using pydirectinput
    def take_action(self, action):
        #action = -1 #π Do not take any action
        if action == 0:
            pydirectinput.keyUp('w')
            pydirectinput.keyUp('s')
            pydirectinput.keyUp('a')
            pydirectinput.keyUp('d')
            #print('πͺ movement released')
        elif action == 1:
            pydirectinput.keyUp('w')
            pydirectinput.keyUp('s')
            pydirectinput.keyDown('w')
        elif action == 2:
            pydirectinput.keyUp('w')
            pydirectinput.keyUp('s')
            pydirectinput.keyDown('s')
        elif action == 3:
            pydirectinput.keyUp('a')
            pydirectinput.keyUp('d')
            pydirectinput.keyDown('a')
        elif action == 4:
            pydirectinput.keyUp('a')
            pydirectinput.keyUp('d')
            pydirectinput.keyDown('d')
        elif action == 5:
            pydirectinput.press('shift')    #dodge
        elif action == 6:
            pydirectinput.press('u')        #light attack
        elif action == 7:
            pydirectinput.press('i')        #heavy attack
        elif action == 8:
            pydirectinput.press('o')        #magic
        elif action == 9 and time.time() - self.time_since_heal > 1.5: #π to prevent spamming heal we only allow it to be pressed every 1.5 seconds
            pydirectinput.press('e')        #item
            self.time_since_heal = time.time()
        #if action != 0:
            #print('πͺ action taken: ' + str(action))
        

    #π This is the function that is called every frame when the agent is training.
    def step(self, action):
        #π Lets look at what step does
        #π 1. Collect the current observation 
        #π 2. Collect the reward based on the observation (reward of previous step)
        #π 3. Check if the game is done (player died, boss died, 10minute time limit reached)
        #π 4. Take the next action (based on the decision of the agent)
        #π 5. Return the observation(img, previous_action, game_state), reward, done, info(empty but required for gym)
        #π 6. train.py decides the next action and calls step again

        #print("πΎ step start")
        if self.first_step: #π If we are in the first step of running this program.
            print("πΎ#1 first step")
            #π Maybe you want some action here...
        
        t0 = time.time()    #π Time of the start of this step
        
        #π 1. Collecting the frame
        frame = self.grab_screen_shot()
        #π 2. Collecting the reward and some other info
        self.reward, self.death, self.boss_death = self.rewardGen.update(frame)
        
        #print('π Reward: ', self.reward)
        #print('π self.death: ', self.death)
        #print('π self.boss_death: ', self.boss_death)

        #π 3. Check if the game is done
        if not self.death:
            #π If we have been in the step loop for more than 10 minutes we give up
            if (time.time() - self.t_start) > 600:
                print('ββ taking too long, giving up...')
                self.take_action(0)
                #π maybe we need a function to warp the player back to spawn if we actually time out
                self.done = True
                print('πΎβοΈ Step done (time limit)')
            elif self.boss_death:
                print('πΎβοΈ Step done (boss dead)')                                                            
                self.done = True 
            #πelif more conditions to end the step loop here:
                #π 1 Boss is lost (for open world bosses maybe)
                #π 2 ...idk
        #π Player death
        else:    #πthis is also called if the health bar disappears due to being out of combat
            print('πΎβοΈ Step done (death)') 
            self.done = True
        
        #π 4. Taking the action
        if not self.done:   #π If we are not done we take the action
            self.take_action(action)
        
            

        #π 5. Wrapping up the step
        observation = cv2.resize(frame, (MODEL_WIDTH, MODEL_HEIGHT))    #π We resize the frame so the agent dosnt have to deal with a 1920x1080 image (400x225)
        #render_frame(observation)                                      #π render the frame for debugging
        info = {}                                                       #π No info to return
        self.first_step = False                                         #π We are no longer on the first step
        self.iteration += 1                                             #π Increment the iteration

        if self.max_reward is None:                                     #π Max reward
            self.max_reward = self.reward
        elif self.max_reward < self.reward:
            self.max_reward = self.reward

        self.reward_history.append(self.reward)                         #π Add the reward to the reward history

        #FPS LIMITER
        t_end = time.time()                                             
        desired_fps = (1 / 24)                                          #π My CPU (i9-13900k) can run the training at about 28FPS max but 24FPS very consistently
        time_to_sleep = desired_fps - (t_end - t0)                      #π We sleep this amount of time to limit the FPS
        #print(1 / (time.time() - t0))
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)
        #END FPS LIMITER
        current_fps = str(round(((1 / (t_end - t0)) * 10), 0))          #π Parsing the current FPS to a string and rounding it so we can print it later 

        #π 5. This is the actual observation that we return
        spaces_dict = {
            'img': observation,
            'prev_actions': oneHotPrevActions(self.action_history),
            'state': np.asarray([self.rewardGen.curr_hp, self.rewardGen.curr_stam])
        }
        
        self.action_history.append(int(action))                                 #π Creating the action history for the next step

        if not self.done:
            #print('πΎ Iteration: ' + str(self.iteration) + '| FPS: ' + current_fps + '| Reward: ' + str(self.reward) + '| Max Reward: ' + str(self.max_reward) + '| Action: ' + str(action))
            #π Making the print pretty
            self.reward = round(self.reward, 0)
            reward_with_spaces = str(self.reward)
            for i in range(4 - len(reward_with_spaces)):
                reward_with_spaces = ' ' + reward_with_spaces
            max_reward_with_spaces = str(self.max_reward)
            for i in range(4 - len(max_reward_with_spaces)):
                max_reward_with_spaces = ' ' + max_reward_with_spaces
            print('πΎ Iteration: ' + str(self.iteration) + '| FPS: ' + current_fps + '| Reward: ' + reward_with_spaces + '| Max Reward: ' + max_reward_with_spaces + '| Action: ' + str(action))
        else:
            print('πΎβοΈ Reward: ' + str(self.reward) + '| Max Reward: ' + str(self.max_reward))
        #π 5. Returning the observation, the reward, if we are done, and the info
        return spaces_dict, self.reward, self.done, info
    

    #π Reset puts the environment back to the initial state so the next episode can start
    def reset(self):
        #π 1. Clear any held down keys
        #π 2. Calculate the average reward for the last run and print it
        #π 3. Checking for loading screen / waiting some time for sucessful reset
        #π 4. Walking back to the boss
        #π 5. Reset all variables
        #π 6. Create the first observation for the next step and return it


        print('π reset called...')
        #π 1.Clear any held down keys
        self.take_action(0)
        print('ππͺ Unholding keys...')

        #π 2. Calculate the average reward for the last run
        if len(self.reward_history) > 0:    #π Calculate the average reward for the last run
            total_r = 0
            for r in self.reward_history:
                total_r += r
            avg_r = total_r / len(self.reward_history)                              
            print('ππ Average reward for last run:', avg_r) 

        
        time.sleep(2)                       #π Waiting 2 seconds to start looking for the loading screen (give the player some time to actually die...)


        #π 3. Checking for loading screen / waiting some time for sucessful reset
        t_check_frozen_start = time.time()  #π Timer to check the time of the loading screen
        loading_screen_flag = False         #π We have not seen the loading screen yet
        t_since_seen_next = None            #π We detect the loading screen by reading the text "next" in the bottom left corner of the loading screen.
        while True: #π We are forever taking a screenshot and checking if it is a loading screen. We break out of this loop when we either decide the game is frozen or we no longer see the loading screen or after 20 seconds
            #π The way we determine if we are in a loading screen is by checking if the text "next" is in the bottom left corner of the screen. If it is we are in a loading screen. If it is not we are not in a loading screen.
            frame = self.grab_screen_shot()
            next_text_image = frame[1015:1040, 155:205]
            next_text_image = cv2.resize(next_text_image, ((205-155)*3, (1040-1015)*3))
            lower = np.array([0,0,75])      #π Making the image black and white to make it easier for pytesseract to read the text
            upper = np.array([255,255,255])
            hsv = cv2.cvtColor(next_text_image, cv2.COLOR_RGB2HSV)
            mask = cv2.inRange(hsv, lower, upper)
            #matches = np.argwhere(mask==255)
            #percent_match = len(matches) / (mask.shape[0] * mask.shape[1])
            #print(percent_match)       #π Percentage of white pixels in the mask
            next_text = pytesseract.image_to_string(mask,  lang='eng',config='--psm 6 --oem 3') #π This is where we read the text
            loading_screen = "Next" in next_text or "next" in next_text                         #π Boolean if we see "next" in the text

            #π Maybe we need a frame limiter here?

            if loading_screen:
                print("Loading Screen:", loading_screen) #Loading Screen: True
                loading_screen_flag = True
                t_since_seen_next = time.time()
            else:   #π If we dont see "next" on the screen we are not in the loading screen [anymore]
                if loading_screen_flag:
                    print('Loading screen seen. Walk back to boss will start in 2.5 seconds...')
                else:
                    print('No loading screen. Step loop will start in 20seconds or after loading screen. Please enter a boss arena or die...')
                
            if not t_since_seen_next is None and ((time.time() - t_check_frozen_start) > 7.5) and (time.time() - t_since_seen_next) > 2.5:  #π We were in a loading screen and left it. (Start step after 2.5 seconds not seeling a loading screen)
                print('βοΈ Left loading screen #1')
                break
            elif not t_since_seen_next is None and  ((time.time() - t_check_frozen_start) > 60):                                            #π We have been in a loading screen for 60 seconds. We assume the game is frozen
                print('β Left loading screen #2 (Frozen)')
                #some sort of error handling here...
                break
            elif t_since_seen_next is None and ((time.time() - t_check_frozen_start) > 20):                                                 #π We have not entered a loading screen for 20 seconds. (Start step after 20 seconds for the first try only of training loop)
                print('βοΈ No loading screen found #3')
                break
            #π elif any of the other conditions are met:
                #π we could do something like staying in this loop until we see a full boss health bar then press the lock on key and start the next step loop. this way we would have automatic initiation of the next step.
                #π If we then wait forever in this loop until that happens, we could just leave the game running and it would automatically start the next step when we enter a boss arena.
            #π elif any of the other conditions are met:
                #π or you could put in a manual break condition here that you set in a different thread. Maybe if you want to use your computer while the game is running you could set a break condition that you can set with a hotkey.
                #π if you also set self.done = True here, the environment will reset and stop moving the character.
        

        #π 3. Walking to the boss
        if loading_screen_flag == True:     #π If we have left the loading screen, we walk to the boss
            print("ππΉ walking to boss")
            walk_to_boss()                  #π This is hard coded in walkToBoss.py

        #π 4. Reset all variables
        self.iteration = 0
        self.reward_history = [] 
        self.done = False
        self.first_step = True
        #self.locked_on = False                             #βοΈ Unused
        self.max_reward = None
        #self.rewardGen.seen_boss = False                   #βοΈ Maybe for open world bosses?
        #self.rewardGen.time_since_seen_boss = time.time()  #βοΈ Unused
        self.rewardGen.prev_hp = 1
        self.rewardGen.curr_hp = 1
        #self.rewardGen.time_since_reset = time.time()      #βοΈ Unused
        #self.rewardGen.time_since_dmg_healed = time.time() #βοΈ Unused
        self.rewardGen.time_since_dmg_taken = time.time()
        #self.rewardGen.hits_taken = 0                      #βοΈ Unused
        self.rewardGen.curr_boss_hp = 1                     #π Reset the boss hp to 100%
        self.rewardGen.prev_boss_hp = 1
        self.t_start = time.time()                          #π Reset the start time for the next run


        #π 5. Return the first observation
        observation = cv2.resize(frame, (MODEL_WIDTH, MODEL_HEIGHT))#π Reset also returns the first observation for the agent
        self.action_history = []
        spaces_dict = { 
            'img': observation,                                     #π The image
            'prev_actions': oneHotPrevActions(self.action_history), #π Empty
            'state': np.asarray([1.0, 1.0])                         #π Full hp and full stamina
        }
        
        print('πβοΈ Reset done.')
        return spaces_dict                                          #π And return the new observation

    #π We never render from inside train.py but gym requires this function
    def render(self, mode='human'):
        pass

    #π Idk if this is even working but we dont call in in ./train.py so it doesnt matter
    def close (self):
        self.cap.release()





