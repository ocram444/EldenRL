import train

if __name__ == '__main__':
    '''User Settings'''
    config = {
        "PYTESSERACT_PATH": r'C:\Program Files\Tesseract-OCR\tesseract.exe',    # Set the path to PyTesseract
        "MONITOR": 1,           #Set the monitor to use (1,2,3)
        "DEBUG_MODE": False,    #Renders the AI vision (pretty scuffed)
        "GAME_MODE": "PVE",     #PVP or PVE
        "BOSS": 3,              #1-6 for PVE (look at walkToBoss.py for boss names) | Is ignored for GAME_MODE PVP
        "PLAYER_HP": 396,      #Set the player hp (used for hp bar detection)
        "PLAYER_STAMINA": 95,  #Set the player stamina (used for stamina bar detection)
        "DESIRED_FPS": 24       #Set the desired fps (used for actions per second) (24 = 2.4 actions per second) #not implemented yet       #My CPU (i9-13900k) can run the training at about 2.4SPS (steps per secons)
    }
    CREATE_NEW_MODEL = False     #Create a new model or resume training for an existing model

    
    '''Start Training'''
    print("💍 EldenRL 💍")
    train.train(CREATE_NEW_MODEL, config)





    # This is what an update looks like.
    # Now the model is saved and can be loaded and further trained.
    # Alright thats it for this video. Thanks for watching and see you in the next one.