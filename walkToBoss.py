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

def put_on_lantern():
        pydirectinput.press('esc')
        time.sleep(0.5)
        #right arrow
        pydirectinput.press('right')
        time.sleep(0.5)
        #e
        pydirectinput.press('e')
        time.sleep(1.5)
        #esc
        pydirectinput.press('esc')
        time.sleep(0.5)






#1 Margit, The fell Omen
def walk_to_boss(BOSS):
        put_on_lantern()
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



'''
#2 Beastman of Farum Azula
def walk_to_boss():     #This can go into a seperate file                                             #📍 This is hard coded for every boss
        put_on_lantern()
        print("👉👹 walking #0 from the bonfire")
        pydirectinput.keyDown('w')
        pydirectinput.keyDown('a')
        time.sleep(1.2)
        pydirectinput.keyUp('a')
        time.sleep(2.5)
        pydirectinput.keyDown('d')
        time.sleep(0.5)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('a')
        time.sleep(0.2)
        pydirectinput.keyUp('a')
        time.sleep(4)
        print("👉👹 walking #1 around the corner")
        pydirectinput.keyDown('d')
        time.sleep(1)
        pydirectinput.keyUp('d')
        time.sleep(3)
        print("👉👹 walking #2 start sprinting")
        pydirectinput.keyDown('shift')
        time.sleep(2.5)
        print("👉👹 walking #3 to the fog gate")
        pydirectinput.keyDown('d')
        time.sleep(0.7)
        pydirectinput.keyUp('d')
        time.sleep(2)
        pydirectinput.keyDown('a')
        time.sleep(0.5)
        pydirectinput.keyUp('a')
        time.sleep(1)
        pydirectinput.keyDown('a')
        time.sleep(0.2)
        pydirectinput.keyUp('a')
        time.sleep(0.6)
        pydirectinput.keyUp('shift')
        pydirectinput.keyUp('w')
        pydirectinput.press('f')
        time.sleep(3.7)
        print("👉👹 walking #4 lock on to the boss")
        pydirectinput.keyDown('w')
        pydirectinput.press('tab')
        time.sleep(1)
        pydirectinput.keyUp('w')
'''



"""
#3 Scally misbegotten   (⚔️ Slain)
def walk_to_boss():
        put_on_lantern()
        print("👉👹 walking #0 from the bonfire")
        pydirectinput.keyDown('shift')
        pydirectinput.keyDown('w')
        time.sleep(4)
        pydirectinput.keyDown('a')
        print("👉👹 walking #1 around the corner")
        time.sleep(1.5)
        pydirectinput.keyUp('a')
        print("👉👹 walking #2 fall down ledge")
        time.sleep(8)
        pydirectinput.keyDown('a')
        print("👉👹 walking #3 around the corner")
        time.sleep(1.3)
        pydirectinput.keyUp('a')
        print("👉👹 walking #4 to the fog gate")
        time.sleep(8)
        pydirectinput.keyUp('w')
        pydirectinput.keyUp('shift')
        pydirectinput.press('f')
        time.sleep(3.2)
        print("👉👹 walking #1 lock on to the boss")
        pydirectinput.keyDown('w')
        pydirectinput.press('shift')
        time.sleep(1)
        pydirectinput.keyUp('w')
        pydirectinput.press('tab')
        print("👉👹 walking done")
"""
"""
#4 Patches      (⚔️ Slain) (buggy)
def walk_to_boss():
        put_on_lantern()
        print("👉👹 walking #0 from the bonfire")
        pydirectinput.keyDown('shift')
        pydirectinput.keyDown('w')
        time.sleep(2.1)
        print("👉👹 walking #1 around the corner")
        pydirectinput.keyDown('d')
        time.sleep(0.6)
        pydirectinput.keyUp('d')
        time.sleep(0.35)
        pydirectinput.keyDown('d')
        time.sleep(0.3)
        pydirectinput.keyUp('d')
        time.sleep(0.8)
        print("👉👹 walking #2 around that same corner")
        pydirectinput.keyDown('d')
        time.sleep(0.4)
        pydirectinput.keyUp('d')
        time.sleep(0.1)
        pydirectinput.keyDown('d')      
        time.sleep(0.1)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('a')
        time.sleep(0.4)
        pydirectinput.keyUp('a')
        print("👉👹 walking #3 walking straight")
        time.sleep(3)
        print("👉👹 walking #4 around the corner")
        pydirectinput.keyDown('d')
        time.sleep(1.8)
        print("👉👹 walking #5 down the path")
        pydirectinput.keyUp('d')
        time.sleep(2.5)
        print("👉👹 walking #6 to the fog gate")
        pydirectinput.keyDown('d')
        time.sleep(0.5)
        pydirectinput.keyUp('d')
        time.sleep(2)

        pydirectinput.keyUp('w')
        pydirectinput.keyUp('shift')
        pydirectinput.press('f')
        time.sleep(3.7)
        print("👉👹 walking #7 lock on to the boss")
        pydirectinput.keyDown('w')
        time.sleep(1.2)
        pydirectinput.keyUp('w')
        pydirectinput.press('tab')
        print("👉👹 walking done")
        """

#4 Erdtree burrial watchdog
'''
def walk_to_boss():
        put_on_lantern()
        print("👉👹 walking #0 from the bonfire")
        pydirectinput.keyDown('shift')
        pydirectinput.keyDown('w')
        time.sleep(4.1)
        print("👉👹 walking #1 around the corner")
        pydirectinput.keyDown('d')
        time.sleep(1.7)
        pydirectinput.keyUp('d')
        print("👉👹 walking #2 to the fog gate")
        time.sleep(10)
        pydirectinput.keyUp('w')
        pydirectinput.keyUp('shift')
        pydirectinput.press('f')
        time.sleep(3.7)
        print("👉👹 walking #3 lock on to the boss")
        pydirectinput.keyDown('w')
        time.sleep(0.5)
        pydirectinput.keyUp('w')
        pydirectinput.press('tab')
        print("👉👹 walking done")
'''

'''
#5 Graven warden duelist        (badly buggy)
def walk_to_boss():
        put_on_lantern()
        print("👉👹 walking #0 from the bonfire")
        pydirectinput.keyDown('shift')
        pydirectinput.keyDown('w')
        time.sleep(8.3)
        print("👉👹 walking #1 around the corner")
        pydirectinput.keyDown('d')
        time.sleep(1.76)
        pydirectinput.keyUp('d')
        print("👉👹 walking #2 down the hallway")
        time.sleep(1.5)
        pydirectinput.keyUp('shift')
        time.sleep(0.9)
        print("👉👹 walking #3 spam dodge")
        pydirectinput.keyUp('shift')
        pydirectinput.press('shift')
        time.sleep(0.1)
        pydirectinput.press('shift')
        time.sleep(0.15)
        pydirectinput.press('shift')
        time.sleep(0.15)
        pydirectinput.press('shift')
        time.sleep(0.1)
        pydirectinput.press('shift')
        pydirectinput.keyDown('w')
        pydirectinput.keyDown('shift')
        time.sleep(6)
        pydirectinput.keyUp('w')
        pydirectinput.keyUp('shift')
        pydirectinput.press('f')
        time.sleep(3.7)
        print("👉👹 walking #4 lock on to the boss")
        pydirectinput.press('tab')
        pydirectinput.keyDown('w')
        time.sleep(0.5)
        pydirectinput.keyUp('w')
        print("👉👹 walking done")
'''

'''
#6 Mad Punpkinhead
def walk_to_boss():
        put_on_lantern()
        print("👉👹 walking #0 from the bonfire")
        pydirectinput.keyDown('shift')
        pydirectinput.keyDown('w')
        time.sleep(2)
        print("👉👹 walking #1 to the ruins")
        pydirectinput.keyDown('d')
        time.sleep(1)
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('a')
        time.sleep(0.85)
        pydirectinput.keyUp('a')
        time.sleep(1.8)
        print("👉👹 walking #2 into the basement")
        pydirectinput.keyUp('shift')
        pydirectinput.keyDown('a')
        time.sleep(1.5)
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('d')
        time.sleep(4)
        pydirectinput.keyUp('d')
        time.sleep(4.5)
        pydirectinput.keyUp('w')
        pydirectinput.keyUp('shift')
        pydirectinput.press('f')
        time.sleep(3.7)
        print("👉👹 walking #3 lock on to the boss")
        pydirectinput.press('tab')
        time.sleep(0.1)
        print("👉👹 walking done")
'''







#🐜 Run the function to test it

def test():
    print("👉👹 3")
    time.sleep(1)
    print("👉👹 2")
    time.sleep(1)
    print("👉👹 1")
    time.sleep(1)
    walk_to_boss()

if __name__ == "__main__":
    test()
