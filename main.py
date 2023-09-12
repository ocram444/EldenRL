import train

if __name__ == '__main__':
    '''User Settings'''
    PYTESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Set the path
    RESUME_TRAINING = True     #Start training from a saved model or create a new model
    DEBUG_MODE = False          #Renders the AI vision (pretty scuffed)
    GAME_MODE = "PVP"           #PVP or PVE
    BOSS = 1                    #1-6 for PVE (look at walkToBoss.py for boss names) | Is ignored for GAME_MODE PVP
    PLAYER_HP = 2140            #Set the player hp (used for hp bar detection)
    PLAYER_STAMINA = 118        #Set the player stamina (used for stamina bar detection)
    DESIRED_FPS = 24            #Set the desired fps (used for actions per second) (24 = 2.4 actions per second) #not implemented yet       #My CPU (i9-13900k) can run the training at about 2.4SPS (steps per secons)
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