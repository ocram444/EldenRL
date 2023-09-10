import train

if __name__ == '__main__':
    '''User Settings'''
    RESUME_TRAINING = False     #Start training from a saved model or create a new model
    DEBUG_MODE = False          #Renders the AI vision
    GAME_MODE = "PVP"           #PVP or PVE
    BOSS = 1                    #1-6 for PVE (look at walkToBoss.py for boss names) | Is ignored for GAME_MODE PVP
    
    '''Start Training'''
    print("💍 EldenRL 💍")
    train.train(RESUME_TRAINING, DEBUG_MODE)