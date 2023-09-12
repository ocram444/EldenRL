import train

if __name__ == '__main__':
    '''User Settings'''
    PYTESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Set the path
    RESUME_TRAINING = False     #Start training from a saved model or create a new model
    DEBUG_MODE = False          #Renders the AI vision (pretty scuffed)

    GAME_MODE = "PVP"           #PVP or PVE
    BOSS = 1                    #1-6 for PVE (look at walkToBoss.py for boss names) | Is ignored for GAME_MODE PVP
    PLAYER_HP = 2140             #Set the player hp (used for hp bar detection)
    PLAYER_STAMINA = 118         #Set the player stamina (used for stamina bar detection)
    DESIRED_FPS = 24            #Set the desired fps (used for actions per second) (24 = 2.4 actions per second) #not implemented yet
    MONITOR = 1                 #Set the monitor to use (1,2,3)

    config = {
        "PYTESSERACT_PATH": PYTESSERACT_PATH,
        "DEBUG_MODE": DEBUG_MODE,
        "GAME_MODE": GAME_MODE,
        "BOSS": BOSS,
        "PLAYER_HP": PLAYER_HP,
        "PLAYER_STAMINA": PLAYER_STAMINA,
        "DESIRED_FPS": DESIRED_FPS,
        "MONITOR": MONITOR
    }

    
    '''Start Training'''
    print("💍 EldenRL 💍")
    train.train(RESUME_TRAINING, config)


#🚦 OK here is what you need to do to run this:
    #🚦 0. Import what you need (keep in mind that you need to install python 3.9 and select it as the python interpreter. And some other stuff that is not just a simple pip install...)
    #🚦 1. Pick Mage starting class and create a new character. Equip left hand staff, right hand sword, only one spell, and only the healing flasks.
    #🚦 2. Start the game and load the character (and walk to a fog gate of the boss you want to fight)
    #🚦 3. Put the game in the top left corner of the screen and make it windowed 1920x1080 (its not to the very left of the screen. There is a small gap. You can render the screenshot to make sure its positioned correctly)
    #🚦 4. Run train.py 
    #🚦 5. The training will start in the reset function...
    #🚦 5.1 The reset function looks for a loading screen and resets the game by walking back to the boss. (It will also end after 20seconds of not seeing a loading screen)
    #🚦 5.2 When the reset function is done, the agent will take over and start taking actions
    #🚦 5.3 The step function will repeat and take actions until it is determined to be done (the agent dies, the boss dies, or the fight takes more than 10minutes)
    #🚦 6 train.py will then save the model and start the next episode (the next reset)
#||| Move this to the readme file |||