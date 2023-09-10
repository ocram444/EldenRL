import cv2
import numpy as np
import time


class EldenReward:
    '''Reward Class'''


    '''Constructor'''
    def __init__(self, DEBUG_MODE, player_hp, player_stamina):
        self.DEBUG_MODE = DEBUG_MODE
        self.max_hp = player_hp                           #This is the hp value of your character(9 vigor). We need this to capture the right length of the hp bar.
        self.prev_hp = 1.0     
        self.curr_hp = 1.0
        self.time_since_dmg_taken = time.time()
        self.death = False
        self.max_stam = player_stamina                     
        self.curr_stam = 1.0
        self.curr_boss_hp = 1.0
        self.prev_boss_hp = 1.0
        self.time_since_boss_dmg = time.time() 
        self.boss_death = False        
        self.image_detection_tolerance = 0.02       #The image detection of the hp bar is not perfect. So we ignore changes smaller than this value. (0.02 = 2%)


    '''Detecting the current player hp'''
    def get_current_hp(self, frame):
        HP_RATIO = 0.403                                                        #Constant to calculate the length of the hp bar
        hp_image = frame[51:53, 155:155 + int(self.max_hp * HP_RATIO) - 20]     #Cut out the hp bar from the frame
        if self.DEBUG_MODE: self.render_frame(hp_image)
        
        lower = np.array([0,90,75])                                             #Filter the image for the correct shade of red
        upper = np.array([150,255,125])                                         #Also Filter
        hsv = cv2.cvtColor(hp_image, cv2.COLOR_RGB2HSV)                         #Apply the filter
        mask = cv2.inRange(hsv, lower, upper)                                   #Also apply
        if self.DEBUG_MODE: self.render_frame(mask)

        matches = np.argwhere(mask==255)                                        #Number for all the white pixels in the mask
        curr_hp = len(matches) / (hp_image.shape[1] * hp_image.shape[0])        #Calculating percent of white pixels in the mask (current hp in percent)

        curr_hp += 0.02         #Adding +2% of hp for color noise

        if curr_hp >= 0.96:     #If the hp is above 96% we set it to 100% (also color noise fix)
            curr_hp = 1.0

        if self.DEBUG_MODE: print('💊 Health: ', curr_hp)
        return curr_hp


    '''Detecting the current player stamina'''
    def get_current_stamina(self, frame):
        STAM_RATIO = 3.0                                                        #Constant to calculate the length of the stamina bar
        stam_image = frame[86:89, 155:155 + int(self.max_stam * STAM_RATIO) - 20] #Cut out the stamina bar from the frame
        if self.DEBUG_MODE: self.render_frame(stam_image)

        lower = np.array([6,52,24])                                             #This filter really inst perfect but its good enough bcause stamina is not that important
        upper = np.array([74,255,77])                                           #Also Filter
        hsv = cv2.cvtColor(stam_image, cv2.COLOR_RGB2HSV)                       #Apply the filter
        mask = cv2.inRange(hsv, lower, upper)                                   #Also apply
        if self.DEBUG_MODE: self.render_frame(mask)

        matches = np.argwhere(mask==255)                                        #Number for all the white pixels in the mask
        self.curr_stam = len(matches) / (stam_image.shape[1] * stam_image.shape[0]) #Calculating percent of white pixels in the mask (current stamina in percent)

        self.curr_stam += 0.02                                                  #Adding +2% of stamina for color noise
        if self.curr_stam >= 0.96:                                              #If the stamina is above 96% we set it to 100% (also color noise fix)
            self.curr_stam = 1.0 

        if self.DEBUG_MODE: print('🏃 Stamina: ', self.curr_stam)
        return self.curr_stam
    

    '''Detecting the current boss hp'''
    def get_boss_hp(self, frame):
        boss_hp_image = frame[867:870, 462:1462]                                #cutting frame for boss hp bar (always same size)
        if self.DEBUG_MODE: self.render_frame(boss_hp_image)

        lower = np.array([0,130,0])                                             #Filter the image for the correct shade of green
        upper = np.array([255,255,255])
        hsv = cv2.cvtColor(boss_hp_image, cv2.COLOR_RGB2HSV)                    #Apply the filter
        mask = cv2.inRange(hsv, lower, upper)
        if self.DEBUG_MODE: self.render_frame(mask)

        matches = np.argwhere(mask==255)                                        #Number for all the white pixels in the mask
        boss_hp = len(matches) / (boss_hp_image.shape[1] * boss_hp_image.shape[0])  #Calculating percent of white pixels in the mask (current boss hp in percent)
        
        #same noise problem but the boss hp bar is larger so noise is less of a problem

        if self.DEBUG_MODE: print('👹 Boss HP: ', boss_hp)

        return boss_hp
    

    '''Debug function to render the frame'''
    def render_frame(self, frame):
        cv2.imshow('debug-render', frame)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

 
    '''Update function that gets called every step and returns the total reward and if the agent died or the boss died'''
    def update(self, frame):
        #📍 0 Getting current values
        #📍 1 Hp Rewards
        #📍 2 Boss Rewards
        #📍 3 PvP Rewards
        #📍 4 Total Reward / Return


        '''📍0 Getting/Setting current values'''
        self.curr_hp = self.get_current_hp(frame)                   
        self.curr_stam = self.get_current_stamina(frame)            
        self.curr_boss_hp = self.get_boss_hp(frame)           

        self.death = False
        if self.curr_hp <= 0.01 + self.image_detection_tolerance:   #If our hp is below 1% we are dead
            self.death = True
            self.curr_hp = 0.0

        self.boss_death = False
        if self.curr_boss_hp <= 0.01:                             #If the boss hp is below 1% the boss is dead (no tolerance because we want to be sure the boss is actually dead)
            self.boss_death = True

        
        '''📍 1 Hp Rewards'''
        hp_reward = 0
        if not self.death:                           
            if self.curr_hp > self.prev_hp + self.image_detection_tolerance:        #Reward if we healed)
                hp_reward = 100                  
            elif self.curr_hp < self.prev_hp - self.image_detection_tolerance:      #Negative reward if we took damage
                hp_reward = -69
                self.time_since_dmg_taken = time.time()
        else:
            hp_reward = -420                                                        #Large negative reward for dying

        time_since_taken_dmg_reward = 0                                    
        if time.time() - self.time_since_dmg_taken > 7:                             #Reward if we have not taken damage for 7 seconds (every step for as long as we dont take damage)
            time_since_taken_dmg_reward = 25


        self.prev_hp = self.curr_hp     #Update prev_hp to curr_hp


        '''📍 2 Boss Rewards'''
        boss_dmg_reward = 0
        if self.boss_death:                                                         #Large reward if the boss is dead
            boss_dmg_reward = 420
        else:
            if self.curr_boss_hp < self.prev_boss_hp - self.image_detection_tolerance  + 0.01:            #Reward if we damaged the boss (small tolerance because its a large bar)
                boss_dmg_reward = 69
                self.time_since_boss_dmg = time.time()
            if time.time() - self.time_since_boss_dmg > 5:                          #Negative reward if we have not damaged the boss for 5 seconds (every step for as long as we dont damage the boss)
                boss_dmg_reward = -25                                               
        

        percent_through_fight_reward = 0
        if self.curr_boss_hp < 0.97:                                                #Increasing reward for every step we are alive depending on how low the boss hp is
            percent_through_fight_reward = self.curr_boss_hp * 100 


        self.prev_boss_hp = self.curr_boss_hp   #Update prev_boss_hp to curr_boss_hp


        '''📍 3 PVP rewards'''
        """
        dodge_reward = 0
        #dodge reward will be hard to implement if we dont just want the agent to spam dodge. So this will be on hold for now

        boss_found_reward = 0
        #maybe for open world bosses?

        time_alive_reward = 0
        #time alive reward will be hard to implement if we dont just want the agent to run away and survive. So this will be on hold for now
        """


        '''📍 4 Total Reward / Return'''
        total_reward = hp_reward + boss_dmg_reward + time_since_taken_dmg_reward + percent_through_fight_reward
        total_reward = round(total_reward, 3)

        return total_reward, self.death, self.boss_death
        




