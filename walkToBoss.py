import pydirectinput
import time

#these walking back functions are hard coded for every boss
#📍 1. Walk to the boss
#📍 2. (optional) Enter the fog gate
#📍 3. Lock on to the boss

#📍 Like everything in this project this is pretty scuffed... 
#📍 The player dosnt always spawn at exactly the same position so sometimes the walking back function will fail. You can probably write a perfect walking back function for every boss but I cant...

"""📍 Controls
                    'w': 'run_forwards',                
                    's': 'run_backwards',
                    'a': 'run_left',
                    'd': 'run_right',
                    'shift': 'dodge',
                    'u': 'attack',
                    'i': 'strong_attack',
                    'o': 'magic',
                    'e': 'use_item'
                    'f': 'enter_fog_gate'
"""


"""
#1 Beastman of Farum Azula  (watch out this dosnt actually work)
def walk_to_boss():     #This can go into a seperate file                                             #📍 This is hard coded for every boss
        print("👉👹 walking #0 down up to the wolf")
        pydirectinput.keyDown('shift')
        pydirectinput.keyDown('w')
        pydirectinput.keyDown('a')
        time.sleep(0.8)
        pydirectinput.keyUp('a')
        time.sleep(6)
        pydirectinput.keyDown('d')
        time.sleep(0.8)
        pydirectinput.keyUp('d')
        time.sleep(4)
        print("👉👹 walking #1 at the wolf")
        pydirectinput.keyDown('d')
        time.sleep(0.5)
        pydirectinput.keyUp('d')
        time.sleep(3)
        print("👉👹 walking #2 to the fog gate")
        pydirectinput.keyDown('a')
        time.sleep(0.5)
        pydirectinput.keyUp('a')
        time.sleep(2)
        pydirectinput.keyDown('a')
        time.sleep(0.5)
        pydirectinput.keyUp('a')
        pydirectinput.keyUp('w')
        pydirectinput.keyUp('shift')
        pydirectinput.press('f')
        time.sleep(3)
        print("👉👹 walking #3 lock on to the boss")
        pydirectinput.keyDown('w')
        time.sleep(0.8)
        pydirectinput.keyUp('w')
        pydirectinput.press('tab')
        print("👉👹 walking done")
"""


#2 Margit, The fell Omen
def walk_to_boss():
        print("👉👹 walking #0 to the fog gate")
        pydirectinput.keyDown('shift')
        pydirectinput.keyDown('w')
        pydirectinput.keyDown('d')
        time.sleep(0.5)
        pydirectinput.keyUp('d')
        time.sleep(2.5)
        pydirectinput.keyDown('d')
        time.sleep(0.7)
        pydirectinput.keyUp('d')
        time.sleep(0.5)
        pydirectinput.keyUp('w')
        pydirectinput.keyUp('shift')
        pydirectinput.press('f')
        time.sleep(3)
        print("👉👹 walking #1 lock on to the boss")
        pydirectinput.keyDown('w')
        time.sleep(0.8)
        pydirectinput.keyUp('w')
        pydirectinput.press('tab')
        print("👉👹 walking done")






#🐜 Run the function to test it
"""
def test():
    print("👉👹 3")
    time.sleep(1)
    print("👉👹 2")
    time.sleep(1)
    print("👉👹 1")
    time.sleep(1)
    walk_to_boss()
test()
"""
