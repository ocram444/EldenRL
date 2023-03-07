import cv2
import numpy as np
import time


def render_frame(frame):                #📍 This is just for debugging purposes. It renders a cv2 image. Use it to make sure your game is being captured correctly.
    cv2.imshow('debug-render', frame)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()


"""
HP_CHART = {}
#📍  saving the vigor chart from the csv file into variables
with open('vigor_chart.csv', 'r') as v_chart:
    for line in v_chart.readlines():
        stat_point = int(line.split(',')[0])
        hp_amount = int(line.split(',')[1])
        HP_CHART[stat_point] = hp_amount
"""


#📝 To do:
#📝 Implement the vigor-hp csv file and make sure it works with the hp bar detection
#📝 Same for stamina
#📝 Finally fix the health bar reading. Computer vision is weird...


class EldenReward:
    #📍 Constructor
    def __init__(self) -> None:  #📍 I dont know what -> None means
        #📍 0 Unused variables
        #self.previous_runes_held = None    #✂️ Unused (maybe later)
        #self.current_runes_held = None     #✂️ Unused
        #self.seen_boss = False             #✂️ Unused
        #self.time_since_seen_boss = time.time()    #📍 this could be used for open world bosses.   #✂️ Unused
        #self.hp_history = []                                                #📍 Could be used so the agent can learn about healing and damage over time. #✂️ Unused

        #📍 1 Player variables
        self.max_hp = 396      #📍 This is the hp value of your character(9 vigor). We need this to capture the right length of the hp bar. #📝 Ideally we create a function that takes the vigor stat of the player and returns the max hp.
        self.prev_hp = 1.0     
        self.curr_hp = 1.0
        self.time_since_dmg_taken = time.time()
        self.death = False
        self.curr_stam = 1.0   #📍 Stamina
        
        #📍 2 Boss variables
        self.curr_boss_hp = 1.0
        self.prev_boss_hp = 1.0
        self.time_since_boss_dmg = time.time() 
        self.boss_death = False        

        #📍 3 Other
        self.image_detection_tolerance = 0.02          #📍 The image detection of the hp bar is not perfect. This is the tolerance for rewards. We need it to make sure we really did take damage and its not just the noise

    #📍 Methods
    def get_current_hp(self, frame):        #📍 Detects and returns the current hp of the player
        #self.rewardGen.max_hp = 100                                            #✒️ Some constant to determine the hp bar length based on the vigor stat (is set in the constructor. This is what needs to change based on the vigor stat)
        hp_ratio = 0.403                                                        #✒️ Some constant to determine the hp bar length based on the vigor stat
        hp_image = frame[51:53, 155:155 + int(self.max_hp * hp_ratio) - 20]     #✒️ Cut out the hp bar from the frame
        #render_frame(hp_image)                                                 #🐜 render the frame for debugging (keep in mind its only 2px high. You wont see much)
        lower = np.array([0,90,75])                                             #✒️ (blue, red, green) Red allowed range of what is considered hp in the image
        upper = np.array([150,255,125])                                         #✒️ uppder limit of the red range
        hsv = cv2.cvtColor(hp_image, cv2.COLOR_RGB2HSV)                         #✒️ Convert the image to hsv
        mask = cv2.inRange(hsv, lower, upper)                                   #✒️ apply the color range
        #render_frame(mask)                                                     #🐜 render the mask for debugging
        matches = np.argwhere(mask==255)                                        #✒️ Number for all the white pixels in the mask
        curr_hp = len(matches) / (hp_image.shape[1] * hp_image.shape[0])        #✒️ Actually calculating a clean 0 to 1 hp value (0.5 = 50% hp)

        curr_hp += 0.02         #📝Quick fix for color noise...           #📝 This could cause issues with the death detection... but this is a problem for later...
        if curr_hp >= 0.96:     #📝Quick fix because I am too stupid to set the colors limits of the health bar correctly. I always get some weird noise in the image and never get 100% hp even if the hp bar is full
            curr_hp = 1.0

        #print('💊 Health: ', curr_hp)  #🐜
        return curr_hp

    def get_current_stamina(self, frame):
        stam_image = frame[86:89, 155:155 + 279]                                    #📍 Cutting the frame to get the stamina bar #📝 This is a hardcoded value. It needs to be changed to a dynamic value based on the endurance stat
        #render_frame(stam_image)    #🐜 render the frame for debugging
        lower = np.array([0,100,0])                                        #✒️ Damn I really hate this stupid color limit thing. Why isnt this (red, green, blue) like in every other program??
        upper = np.array([150,255,150])
        hsv = cv2.cvtColor(stam_image, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        #render_frame(mask)    #🐜 render the frame for debugging
        matches = np.argwhere(mask==255)
        self.curr_stam = len(matches) / (stam_image.shape[1] * stam_image.shape[0]) #📍 Calculating the current stamina value

        #dumb quick fix for color noise
        self.curr_stam += 0.02
        if self.curr_stam >= 0.96:
            self.curr_stam = 1.0
        #print('🏃 Stamina: ', self.curr_stam)
        return self.curr_stam
    

    def get_boss_hp(self, frame):
        boss_hp_image = frame[867:870, 462:1462]                                    #📍 cutting frame for boss hp bar
        #render_frame(boss_hp_image)    #🐜 render the frame for debugging
        lower = np.array([0,130,0])
        upper = np.array([255,255,255])
        hsv = cv2.cvtColor(boss_hp_image, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        #render_frame(mask)    #🐜 render the frame for debugging
        matches = np.argwhere(mask==255)
        boss_hp = len(matches) / (boss_hp_image.shape[1] * boss_hp_image.shape[0])  #📍 Calculate the boss hp
        #print('👹 Boss HP: ', boss_hp)

        #📝 same noise problem but the boss hp is larger so noise is less of a problem
        return boss_hp

 
    def update(self, frame):
        #📍 0 Getting current values
        self.curr_hp = self.get_current_hp(frame)                   #📍 hp for reward and observation
        self.curr_stam = self.get_current_stamina(frame)            #📍 stamina for observation (yes we could do this in the step function but we already grab the hp here so I'll do this here as well)
        self.curr_boss_hp = self.get_boss_hp(frame)                 #📍 boss hp for reward

        self.death = False
        if self.curr_hp <= 0.01 + self.image_detection_tolerance:   #📍 Detecting if we are dead
            self.death = True
            self.curr_hp = 0.0

        self.boss_death = False
        if self.curr_boss_hp <= 0.01:                               #📍 If the boss is dead we reward a lot
            self.boss_death = True

        
        #📍 1 Hp Rewards
        hp_reward = 0
        if not self.death:                                                          #📍 If we are not dead we calculate the hp reward
            if self.curr_hp > self.prev_hp + self.image_detection_tolerance:        #📍 If we healed we reward (+ 2% tolerance)
                hp_reward = 100                  
            elif self.curr_hp < self.prev_hp - self.image_detection_tolerance:      #📍 If we took damage we punish (- 2% tolerance)
                hp_reward = -69
                self.time_since_dmg_taken = time.time()
            self.prev_hp = self.curr_hp                                             #📍 We update the prev_hp to the current hp
        else:
            hp_reward = -420                                                        #📍 If we are dead we punish a lot

        time_since_taken_dmg_reward = 0                                    
        if time.time() - self.time_since_dmg_taken > 7:                             #📍 If we have not taken damage for 7 seconds we reward
            time_since_taken_dmg_reward = 25                                        #📍 (we aim for 24 frames per second) +1 * 25 reward per second

        #📍


        #📍 2 Boss Rewards
        boss_dmg_reward = 0
        if self.boss_death:                                                         #📍 If the boss is dead we reward a lot
            boss_dmg_reward = 420
        else:
            if self.curr_boss_hp < self.prev_boss_hp - self.image_detection_tolerance  + 0.01:            #📍 If the boss has taken damage we reward (- 1% tolerance) (we need to deal at least 1% damage to get a reward. This could cause problems if we dont deal enough damage...)
                boss_dmg_reward = 69
                self.time_since_boss_dmg = time.time()
            if time.time() - self.time_since_boss_dmg > 5:                          #📍 If the boss has not taken damage for 5 seconds we punish (we want the agent to be aggressive)
                boss_dmg_reward = -25                                               #📍 (we aim for 24 frames per second) -1 reward per second
        self.prev_boss_hp = self.curr_boss_hp                                       #📍 We update the prev_boss_hp to the current boss hp

        percent_through_fight_reward = 0
        if self.curr_boss_hp < 0.97:                                #📍 If the boss is damaged we reward every second for how low the boss is
            percent_through_fight_reward = self.curr_boss_hp * 100 


        #📍 3 Other Rewards
        """
        dodge_reward = 0
        #dodge reward will be hard to implement if we dont just want the agent to spam dodge. So this will be on hold for now

        boss_found_reward = 0
        #maybe for open world bosses?

        
        time_alive_reward = 0
        #time alive reward will be hard to implement if we dont just want the agent to run away and survive. So this will be on hold for now
        """


        #📍 4 Total Reward / Return
        total_reward = hp_reward + boss_dmg_reward + time_since_taken_dmg_reward + percent_through_fight_reward #+ dodge_reward + boss_found_reward + time_alive_reward
        total_reward = round(total_reward, 3)

        return total_reward, self.death, self.boss_death
        