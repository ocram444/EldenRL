import pydirectinput
import time


class walkToBoss:
        '''Walk to boss class - hard coded paths from the bonfire to the boss'''

        '''Constructor'''
        def __init__(self, BOSS):
                self.BOSS = BOSS        #Boss number | 99/100 reserved for PVP


        '''Walk to boss function'''
        def perform(self):
                '''PVE'''
                if self.BOSS == 1:
                        self.boss1()
                elif self.BOSS == 2:
                        self.boss2()
                elif self.BOSS == 3:
                        self.boss3()
                elif self.BOSS == 4:
                        self.boss4()
                elif self.BOSS == 5:
                        self.boss5()
                elif self.BOSS == 6:
                        self.boss6()

                #'''PVP'''
                elif self.BOSS == 99:
                        self.matchmaking()
                elif self.BOSS == 100:
                        self.duel_arena_lockon()

                else:
                        print("👉👹 Boss not found")


        '''Put on lantern'''
        def put_on_lantern(self):
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


        '''1 Margit, The fell Omen'''
        def boss1(self):
                self.put_on_lantern()
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


        '''2 Beastman of Farum Azula'''
        def boss2(self):
                self.put_on_lantern()
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


        '''3 Scally misbegotten'''
        def boss3(self):
                self.put_on_lantern()
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


        '''4 Patches (buggy)'''
        def boss4(self):
                self.put_on_lantern()
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


        '''5 Erdtree burrial watchdog'''
        def boss5(self):
                self.put_on_lantern()
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


        '''6 Graven warden duelist (badly buggy)'''
        def boss6(self):
                self.put_on_lantern()
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


        '''7 Mad Punpkinhead'''
        def boss7(self):
                self.put_on_lantern()
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
        
        '''PvP Matchmaking'''
        def matchmaking(self):
                pydirectinput.press('f')
                time.sleep(0.5)
                pydirectinput.press('up')
                time.sleep(0.5)
                pydirectinput.press('e')
                time.sleep(0.5)
                pydirectinput.press('e')
                print("⚔️ PvP Matchmaking")

        '''PvP Duel Arena Lockon'''
        def duel_arena_lockon(self):
                time.sleep(2)
                pydirectinput.press('tab')
                time.sleep(0.1)
                print("⚔️ Duelist locked on")




#Run the function to test it
def test():
    print("👉👹 3")
    time.sleep(1)
    print("👉👹 2")
    time.sleep(1)
    print("👉👹 1")
    time.sleep(1)
    walkToBoss(1).walk_to_boss()

if __name__ == "__main__":
    test()
