import cv2
import gym
import mss
import time
import numpy as np
from gym import spaces
import pydirectinput
import pytesseract                              # Pytesseract is not just a simple pip install.
from EldenReward import EldenReward
from walkToBoss import walkToBoss


N_CHANNELS = 3                                  #Image format
IMG_WIDTH = 1920                                #Game capture resolution
IMG_HEIGHT = 1080                             
MODEL_WIDTH = int(800 / 2)                      #Ai vision resolution
MODEL_HEIGHT = int(450 / 2)


'''Ai action list'''
DISCRETE_ACTIONS = {'release_wasd': 'release_wasd',
                    'w': 'run_forwards',                
                    's': 'run_backwards',
                    'a': 'run_left',
                    'd': 'run_right',
                    'w+shift': 'dodge_forwards',
                    's+shift': 'dodge_backwards',
                    'a+shift': 'dodge_left',
                    'd+shift': 'dodge_right',
                    'c': 'attack',
                    'v': 'strong_attack',
                    'x': 'magic',
                    'q+c': 'weapon_art_light',
                    'q+v': 'weapon_art_heavy',
                    'w+c': 'running_attack',
                    'w+v': 'running_heavy',
                    'e': 'use_item'}

NUMBER_DISCRETE_ACTIONS = len(DISCRETE_ACTIONS)
NUM_ACTION_HISTORY = 10                         #Number of actions the agent can remember


class EldenEnv(gym.Env):
    """Custom Elden Ring Environment that follows gym interface"""


    def __init__(self, config):
        '''Setting up the environment'''
        super(EldenEnv, self).__init__()

        '''Setting up the gym spaces'''
        self.action_space = spaces.Discrete(NUMBER_DISCRETE_ACTIONS)                                                            #Discrete action space with NUM_ACTION_HISTORY actions to choose from
        spaces_dict = {                                                                                                         #Observation space (img, prev_actions, state)
            'img': spaces.Box(low=0, high=255, shape=(MODEL_HEIGHT, MODEL_WIDTH, N_CHANNELS), dtype=np.uint8),                      #Image of the game
            'prev_actions': spaces.Box(low=0, high=1, shape=(NUM_ACTION_HISTORY, NUMBER_DISCRETE_ACTIONS, 1), dtype=np.uint8),      #Last 10 actions as one hot encoded array
            'state': spaces.Box(low=0, high=1, shape=(2,), dtype=np.float32),                                                       #Stamina and helth of the player in percent
        }
        self.observation_space = gym.spaces.Dict(spaces_dict)
    

        '''Setting up the variables'''''
        pytesseract.pytesseract.tesseract_cmd = config["PYTESSERACT_PATH"]          #Setting the path to pytesseract.exe            
        self.sct = mss.mss()                                                        #Initializing CV2 and MSS (used to take screenshots)
        self.reward = 0                                                             #Reward of the previous step
        self.rewardGen = EldenReward(config)                                        #Setting up the reward generator class
        self.death = False                                                          #If the agent died
        self.duel_won = False                                                       #If the agent won the duel
        self.t_start = time.time()                                                  #Time when the training started
        self.done = False                                                           #If the game is done
        self.step_iteration = 0                                                     #Current iteration (number of steps taken in this fight)
        self.first_step = True                                                      #If this is the first step
        self.max_reward = None                                                      #The maximum reward that the agent has gotten in this fight
        self.reward_history = []                                                    #Array of the rewards to calculate the average reward of fight
        self.action_history = []                                                    #Array of the actions that the agent took.
        self.time_since_heal = time.time()                                          #Time since the last heal
        self.action_name = ''                                                       #Name of the action for logging
        self.MONITOR = config["MONITOR"]                                            #Monitor to use
        self.DEBUG_MODE = config["DEBUG_MODE"]                                      #If we are in debug mode
        self.GAME_MODE = config["GAME_MODE"]                                        #If we are in PVP or PVE mode
        self.DESIRED_FPS = config["DESIRED_FPS"]                                    #Desired FPS (not implemented yet)
        if self.GAME_MODE == "PVE": self.walk_to_boss = walkToBoss(config["BOSS"])  #Class to walk to the boss
        else : 
            self.matchmaking = walkToBoss(99)                           #Matchmaking class for PVP mode
            self.duel_lockon = walkToBoss(100)                          #Lock on class to the player in PVP mode
            self.first_reset = True
    

    '''One hot encoding of the last 10 actions'''
    def oneHotPrevActions(self, actions):
        oneHot = np.zeros(shape=(NUM_ACTION_HISTORY, NUMBER_DISCRETE_ACTIONS, 1))
        for i in range(NUM_ACTION_HISTORY):
            if len(actions) >= (i + 1):
                oneHot[i][actions[-(i + 1)]][0] = 1
        #print(oneHot)
        return oneHot 


    '''Grabbing a screenshot of the game'''
    def grab_screen_shot(self):
        monitor = self.sct.monitors[self.MONITOR]
        sct_img = self.sct.grab(monitor)
        frame = cv2.cvtColor(np.asarray(sct_img), cv2.COLOR_BGRA2RGB)
        frame = frame[46:IMG_HEIGHT + 46, 12:IMG_WIDTH + 12]    #cut the frame to the size of the game
        if self.DEBUG_MODE:
            self.render_frame(frame)
        return frame
    

    '''Rendering the frame for debugging'''
    def render_frame(self, frame):                
        cv2.imshow('debug-render', frame)
        cv2.waitKey(100)
        cv2.destroyAllWindows()
    
    
    '''Defining the actions that the agent can take'''
    def take_action(self, action):
        #action = -1 #Uncomment this for emergency block all actions
        if action == 0:
            pydirectinput.keyUp('w')
            pydirectinput.keyUp('s')
            pydirectinput.keyUp('a')
            pydirectinput.keyUp('d')
            self.action_name = 'stop'
        elif action == 1:
            pydirectinput.keyUp('w')
            pydirectinput.keyUp('s')
            pydirectinput.keyDown('w')
            self.action_name = 'w'
        elif action == 2:
            pydirectinput.keyUp('w')
            pydirectinput.keyUp('s')
            pydirectinput.keyDown('s')
            self.action_name = 's'
        elif action == 3:
            pydirectinput.keyUp('a')
            pydirectinput.keyUp('d')
            pydirectinput.keyDown('a')
            self.action_name = 'a'
        elif action == 4:
            pydirectinput.keyUp('a')
            pydirectinput.keyUp('d')
            pydirectinput.keyDown('d')
            self.action_name = 'd'
        elif action == 5:
            pydirectinput.keyDown('w')
            pydirectinput.press('shift')
            self.action_name = 'dodge-forward'
        elif action == 6:
            pydirectinput.keyDown('s')
            pydirectinput.press('shift')
            self.action_name = 'dodge-backward'
        elif action == 7:
            pydirectinput.keyDown('a')
            pydirectinput.press('shift')
            self.action_name = 'dodge-left'
        elif action == 8:
            pydirectinput.keyDown('d')
            pydirectinput.press('shift')
            self.action_name = 'dodge-right'
        elif action == 9:
            pydirectinput.press('c')
            self.action_name = 'attack'
        elif action == 10:
            pydirectinput.press('v')
            self.action_name = 'heavy'
        elif action == 11:
            pydirectinput.press('x')
            self.action_name = 'magic'
        elif action == 12:                  #weapon art light
            pydirectinput.keyDown('q')
            time.sleep(0.1)
            pydirectinput.press('c')
            pydirectinput.keyUp('q')
            self.action_name = 'weapon art light'
        elif action == 13:                  #weapon art heavy
            pydirectinput.keyDown('q')
            time.sleep(0.1)
            pydirectinput.press('v')
            pydirectinput.keyUp('q')
            self.action_name = 'weapon art heavy'
        elif action == 14:                  #running attack
            pydirectinput.keyDown('shift')
            pydirectinput.keyDown('w')
            time.sleep(0.35)
            pydirectinput.press('c')
            pydirectinput.keyUp('shift')
            self.action_name = 'running attack'
        elif action == 15:                  #running heavy
            pydirectinput.keyDown('shift')
            pydirectinput.keyDown('w')
            time.sleep(0.35)
            pydirectinput.press('v')
            pydirectinput.keyUp('shift')
            self.action_name = 'running heavy'
        elif action == 16 and time.time() - self.time_since_heal > 1.5: #to prevent spamming heal we only allow it to be pressed every 1.5 seconds
            pydirectinput.press('e')        #item
            self.time_since_heal = time.time()
            self.action_name = 'heal'
        elif action == 99:
            pydirectinput.press('esc')
            time.sleep(0.5)
            pydirectinput.press('right')
            time.sleep(0.4)
            pydirectinput.press('right')
            time.sleep(0.4)
            pydirectinput.press('e')
            time.sleep(1.5)
            #esc
            pydirectinput.press('esc')
            time.sleep(0.5)
            print('🔥')


    '''Waiting for the loading screen to end'''
    def wait_for_loading_screen(self):
        in_loading_screen = False           #If we are in a loading screen right now
        have_been_in_loading_screen = False #If a loading screen was detected
        t_check_frozen_start = time.time()  #Timer to check the length of the loading screen
        t_since_seen_next = None            #We detect the loading screen by reading the text "next" in the bottom left corner of the loading screen.
        while True: #We are forever taking a screenshot and checking if it is a loading screen.
            frame = self.grab_screen_shot()
            in_loading_screen = self.check_for_loading_screen(frame)
            if in_loading_screen:
                print("⌛ Loading Screen:", in_loading_screen) #Loading Screen: True
                have_been_in_loading_screen = True
                t_since_seen_next = time.time()
            else:   #If we dont see "next" on the screen we are not in the loading screen [anymore]
                if have_been_in_loading_screen:
                    print('⌛ After loading screen...')
                else:
                    print('⌛ Waiting for loading screen...')
                
            if have_been_in_loading_screen and (time.time() - t_since_seen_next) > 2.5:             #We have been in a loading screen and left it for more than 2.5 seconds
                print('⌛✔️ Left loading screen #1')
                break
            elif have_been_in_loading_screen and  ((time.time() - t_check_frozen_start) > 60):      #We have been in a loading screen for 60 seconds. We assume the game is frozen
                print('⌛❌ Did not leave loading screen #2 (Frozen)')
                #some sort of error handling here...
                #break
            elif not have_been_in_loading_screen and ((time.time() - t_check_frozen_start) > 25):   #We have not entered a loading screen for 25 seconds. (return to bonfire and walk to boss) #⚔️ in pvp we use this for waiting for matchmaking
                print('⌛✔️ No loading screen found #3')
                if self.GAME_MODE == "PVE": 
                    self.take_action(99)                #warp back to bonfire
                    t_check_frozen_start = time.time()  #reset the timer
                                                        #try again by not breaking the loop
                else:
                    t_check_frozen_start = time.time()  #reset the timer
                                                        #continue waiting for loading screen (matchmaking)
        

    '''Checking if we are in a loading screen'''
    def check_for_loading_screen(self, frame):
        #The way we determine if we are in a loading screen is by checking if the text "next" is in the bottom left corner of the screen. If it is we are in a loading screen. If it is not we are not in a loading screen.
        next_text_image = frame[1015:1040, 155:205] #Cutting the frame to the location of the text "next" (bottom left corner)
        next_text_image = cv2.resize(next_text_image, ((205-155)*3, (1040-1015)*3))
        lower = np.array([0,0,75])                  #Removing color from the image
        upper = np.array([255,255,255])
        hsv = cv2.cvtColor(next_text_image, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        pytesseract_output = pytesseract.image_to_string(mask,  lang='eng',config='--psm 6 --oem 3') #reading text from the image cut out
        in_loading_screen = "Next" in pytesseract_output or "next" in pytesseract_output             #Boolean if we see "next" in the text
        
        if self.DEBUG_MODE:
            matches = np.argwhere(mask==255)
            percent_match = len(matches) / (mask.shape[0] * mask.shape[1])
            print(percent_match)

        return in_loading_screen
        

    '''Step function that is called by train.py'''
    def step(self, action):
        #📍 Lets look at what step does
        #📍 1. Collect the current observation 
        #📍 2. Collect the reward based on the observation (reward of previous step)            #⚔️PvP reward
        #📍 3. Check if the game is done (player died, boss died, 10minute time limit reached)  #⚔️Or duel won
        #📍 4. Take the next action (based on the decision of the agent)
        #📍 5. Ending the step
        #📍 6. Returning the observation, the reward, if we are done, and the info
        #📍 7*. train.py decides the next action and calls step again


        if self.first_step: print("🐾#1 first step")
        
        '''Grabbing variables'''
        t_start = time.time()    #Start time of this step
        frame = self.grab_screen_shot()                                         #📍 1. Collect the current observation
        self.reward, self.death, self.boss_death, self.duel_won = self.rewardGen.update(frame) #📍 2. Collect the reward based on the observation (reward of previous step)
        

        if self.DEBUG_MODE:
            print('🎁 Reward: ', self.reward)
            print('🎁 self.death: ', self.death)
            print('🎁 self.boss_death: ', self.boss_death)


        '''📍 3. Checking if the game is done'''
        if self.death:
            self.done = True
            print('🐾✔️ Step done (player death)') 
        else:
            if (time.time() - self.t_start) > 600:  #If the agent has been in control for more than 10 minutes we give up
                self.done = True
                self.take_action(99)                #warp back to bonfire
                print('🐾✔️ Step done (time limit)')
            elif self.boss_death:
                self.done = True   
                self.take_action(99)                #warp back to bonfire
                print('🐾✔️ Step done (boss death)')    
        if self.duel_won:
            self.done = True
            print('🐾✔️ Step done (duel won)')                                            
            

        '''📍 4. Taking the action'''
        if not self.done:
            self.take_action(action)
        

        '''📍 5. Ending the steap'''

        '''Return values'''
        info = {}                                                       #Empty info for gym
        observation = cv2.resize(frame, (MODEL_WIDTH, MODEL_HEIGHT))    #We resize the frame so the agent dosnt have to deal with a 1920x1080 image (400x225)
        if self.DEBUG_MODE: self.render_frame(observation)              #🐜 If we are in debug mode we render the frame
        if self.max_reward is None:                                     #Max reward
            self.max_reward = self.reward
        elif self.max_reward < self.reward:
            self.max_reward = self.reward
        self.reward_history.append(self.reward)                         #Reward history
        spaces_dict = {                                                 #Combining the observations into one dictionary like gym wants it
            'img': observation,
            'prev_actions': self.oneHotPrevActions(self.action_history),
            'state': np.asarray([self.rewardGen.curr_hp, self.rewardGen.curr_stam])
        }


        '''Other variables that need to be updated'''
        self.first_step = False
        self.step_iteration += 1
        self.action_history.append(int(action))                         #Appending the action to the action history


        '''FPS LIMITER'''
        t_end = time.time()                                             
        desired_fps = (1 / self.DESIRED_FPS)                            #My CPU (i9-13900k) can run the training at about 2.4SPS (steps per secons)
        time_to_sleep = desired_fps - (t_end - t_start)
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)
        '''END FPS LIMITER'''


        current_fps = str(round(((1 / (t_end - t_start)) * 10), 0))     #Current SPS (steps per second)


        '''Console output of the step'''
        if not self.done: #Losts of python string formatting to make the console output look nice
            self.reward = round(self.reward, 0)
            reward_with_spaces = str(self.reward)
            for i in range(5 - len(reward_with_spaces)):
                reward_with_spaces = ' ' + reward_with_spaces
            max_reward_with_spaces = str(self.max_reward)
            for i in range(5 - len(max_reward_with_spaces)):
                max_reward_with_spaces = ' ' + max_reward_with_spaces
            for i in range(7 - len(str(self.action_name))):
                self.action_name = ' ' + self.action_name
            for i in range(5 - len(current_fps)):
                current_fps = ' ' + current_fps
            print('👣 Iteration: ' + str(self.step_iteration) + '| FPS: ' + current_fps + '| Reward: ' + reward_with_spaces + '| Max Reward: ' + max_reward_with_spaces + '| Action: ' + str(self.action_name))
        else:           #If the game is done (Logging Reward for dying or winning)
            print('👣✔️ Reward: ' + str(self.reward) + '| Max Reward: ' + str(self.max_reward))


        #📍 6. Returning the observation, the reward, if we are done, and the info
        return spaces_dict, self.reward, self.done, info
    

    '''Reset function that is called if the game is done'''
    def reset(self):
        #📍 1. Clear any held down keys
        #📍 2. Print the average reward for the last run
        #📍 3. Wait for loading screen                      #⚔️3-4 PvP: wait for loading screen - matchmaking - wait for loading screen - lock on
        #📍 4. Walking back to the boss
        #📍 5. Reset all variables
        #📍 6. Create the first observation for the first step and return it


        print('🔄 Reset called...')


        '''📍 1.Clear any held down keys'''
        self.take_action(0)
        print('🔄🔪 Unholding keys...')

        '''📍 2. Print the average reward for the last run'''
        if len(self.reward_history) > 0:
            total_r = 0
            for r in self.reward_history:
                total_r += r
            avg_r = total_r / len(self.reward_history)                              
            print('🔄🎁 Average reward for last run:', avg_r) 


        '''📍 3. Checking for loading screen / waiting some time for sucessful reset'''
        if self.GAME_MODE == "PVE": self.wait_for_loading_screen()
        else:   #⚔️
            #wait for loading screen (after the duel) - matchmaking - wait for loading screen (into the duel) - lock on
            if not self.first_reset:            #handle the first reset differently (we want to start with the matchmaking, not with losing a duel)
                self.wait_for_loading_screen() 
                self.matchmaking.perform()
            self.first_reset = False
            self.wait_for_loading_screen()
            self.duel_lockon.perform()
            

        '''📍 4. Walking to the boss'''         #⚔️we already did this in 📍 3. for PVP
        if self.GAME_MODE == "PVE":               
            print("🔄👹 walking to boss")
            self.walk_to_boss.perform()          #This is hard coded in walkToBoss.py

        if self.death:                           #Death counter in txt file
            f = open("deathCounter.txt", "r")
            deathCounter = int(f.read())
            f.close()
            deathCounter += 1
            f = open("deathCounter.txt", "w")
            f.write(str(deathCounter))
            f.close()


        '''📍 5. Reset all variables'''
        self.step_iteration = 0
        self.reward_history = [] 
        self.done = False
        self.first_step = True
        self.max_reward = None
        self.rewardGen.prev_hp = 1
        self.rewardGen.curr_hp = 1
        self.rewardGen.time_since_dmg_taken = time.time()
        self.rewardGen.curr_boss_hp = 1
        self.rewardGen.prev_boss_hp = 1
        self.action_history = []
        self.t_start = time.time()


        '''📍 6. Return the first observation'''
        frame = self.grab_screen_shot()
        observation = cv2.resize(frame, (MODEL_WIDTH, MODEL_HEIGHT))    #Reset also returns the first observation for the agent
        spaces_dict = { 
            'img': observation,                                         #The image
            'prev_actions': self.oneHotPrevActions(self.action_history),#The last 10 actions (empty)
            'state': np.asarray([1.0, 1.0])                             #Full hp and full stamina
        }
        
        print('🔄✔️ Reset done.')
        return spaces_dict                                              #return the new observation


    '''No render function implemented (just look at the game)'''
    def render(self, mode='human'):
        pass


    '''Closing the environment (not used)'''
    def close (self):
        self.cap.release()

