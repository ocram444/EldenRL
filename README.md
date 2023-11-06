# EldenRL - Elden Ring Ai
Reinforcement Learning for Elden Ring on Windows11.  
  
EldenRL is build on OpenAI's <code>gym</code> toolkit for reinforcement learning environments. It enables training and running of reinforcement learning models on Elden Ring bosses and PvP duels. EldenRL uses the game as a its environment by capturing the screen and controling the game.

![Component 1](https://github.com/ocram444/EldenRL/assets/113638653/4a6ce798-4797-43a1-a48c-1ed20cf88d12)

# Requirements
You need to own and install Elden Ring and set to windowed mode 1920x1080 at the top left of your screen. EldenRL requires the player to load into the game before any training is ran. In addition we require the following key bindings: <code>w,a,s,d = movement | shift = sprint / dodge | c = light attack | v = heavy attack | x = off hand (magic) | q = weapon art | e = item | f = interact | esc = menu</code>.
After the game is installed and set up correctly you can install the code requirenments. Most things are a simple <code>pip installs</code> but there are some special installation to be aware off: <code>Stable-Baselines3</code> requires Python 3.9.13 and PyTorch to run. <code>Pytesseract</code> needs to be downloaded and installed and the path needs to be set in main.py for reading text from images.
This project is built on Windows 11 but should run on older Windows version too.
Apart from the software requirements you will the hardware to run the training. The Project has been tested in CPU mode with the game running normally on the GPU and the training running on the CPU. The tested performance for this is ~2.4fps on a i9 13900k CPU for the training (and the game running normally).


# Running the code
Given you dont want to dive deep into the Code, running this Project should be fairly straight forward.<br>
Download the Repository, install the requiremets and navigate to the <code>main.py</code> file. Set the <code>config</code> variables to the correct values you want them to run on then simply run the code. In the console the programm will output its state and inform you about what is going on. Starting a new training session will look something like this:<br><br>
<img width="639" alt="Screenshot 2023-09-13 135635" src="https://github.com/ocram444/EldenRL/assets/113638653/bacd2df9-6b74-46f9-9280-b5e7f3f11599"><br>
When the code is <code>Waiting for loading screen...</code> you will need to start matchmaking for PvP mode or kill the character to trigger a loading screen in PvE mode.
After the loading screen the code will call <code>WalkToBoss.py</code> and bring the agent to its initial position where the agent can then take over.
Once the agent takes over the console will look something like this:<br><br>
<img width="750" alt="Screenshot 2023-09-13 140829" src="https://github.com/ocram444/EldenRL/assets/113638653/37d1ba39-666c-44ca-a418-1d25e0de1588"><br>
Now the training session should run without any further input from the user in an endless loop.<br>(Loading screen - Reset - Training - Death - Loading screen - ...)


# Saving / Running a model
To create a new model set <code>CREATE_NEW_MODEL</code> in main.py to True, or set it to False after a model has been saved at least once. During training the model will be saved automatically to <code>./models</code> after 500 steps of the agent making decisions. This took about 20 deaths for a newly created model training in PvE. Saving will look like this:<br><br>
<img width="338" alt="Screenshot 2023-09-13 141638" src="https://github.com/ocram444/EldenRL/assets/113638653/b694b237-26ab-43be-a458-f52f4df93434"><br>
Note that a model will perform random actions when its newly created and will only update its behaviour when it is saved.<br>
Logs for Tensorboard logging can be found in <code>./logs</code>.

# Code
In this section we'll go over the code structure and functionality of the Project.

<b>main.py</b><br>
This is the main file that can be run to start the codebase. Most user settings can be found here to make it as simple as possible.

<b>train.py</b><br>
This is the center pice of the whole project. This is where the decision making and training actually happens. It should feel very familiar if youve worked on a Reinforcement Learning project before. For this we closely folloed OpenAI's <code>gym</code> structure.

<b>EldenEnv.py</b><br>
This is our Environment. Here we interact with the game (capturing the screen, performing actions and passing the observation/reward back to train.py).

<b>EldenReward.py</b><br>
This is where we calculate the reward based on the observation. The total reward for every step is passed back to EldenEnv.py.

<b>WalkToBoss.py</b><br>
This is our reset functionality. In PvE it is called to walk the character from the bonfire to the boss, in PvP it handles matchmaking and player lock-on.

# Observation Space
All of our observation are derived from screen capturing the game with CV2. This means the agent can only use information based on that, no reading of game states or reading memory.<br>
The agent has the following information in the observation space:<br>
1. A scaled down image of the game.
2. Player Health and Stamina in percent.
3. A list of 10 previous actions.

For sucessfull screen capture the game needs to be in Windowed mode 1920x1080 at the top left of your screen. We use the default position when the game is truned to window mode, this means there is a small gap to the left border of your monitor. You can set <code>DEBUG_MODE</code> to true to nail the correct position.

# Rewards
The rewards are also all derived from the same screen capture used in the observation. The agent is rewarded/punished for the following things:<br>
PvE:<br>
1. Healing damage: +100
2. Not taking damage for more than 5s: +25 every step
3. Taking damage: -69
4. Dying: -420
5. Dealing damage to boss: +69
6. Killing the boss: +420
7. Not dealing damage to the boss for more than 5s: -25 every step
8. Increasing reward for every step alive depending on how low the boss hp is<br>

PvP:<br>
1. Healing damage: +100
2. Not taking damage for more than 5s: +25 every step
3. Taking damage: -69
4. Dying: -420
5. Dealing damage to enemy: +69
6. Not dealing damage to the enemy for more than 5s: -25 every step
7. Winning the duel: +420


# Notes
- We are not responsible if you get banned for using this bot in PvP! (We havent had any bans yet thought) 
- Open world navigation and bosses arent possible for now.
- Walking to the boss/fog gate is hard coded for every boss.

# Videos<br>
Have a look at the EldenRL showcase to better understand this project.<br>
EldenRL PvE showcase: https://www.youtube.com/watch?v=NzTwDO4ehPY<br>
EldenRL PvP showcase: https://www.youtube.com/watch?v=2Uh1T8FE0y8


# Contribute
This project is fully open source. It was only possible with the help of multiple contributers laying the groundwork for this project. Feel free to use this code in any way you want.
If you want to contribute to this project feel free to fork it and let us know on the Discord server.

The next steps would probably be to train a modle for longer than we have and measuring some results. Then adding some new rewards or improving the observations could be a logical next step. Its also possible to swap out reinforcement learning modles with stable_baselines_3 and comparing the results between them.

Huge shoutout to Jameszampa and Lockwo for doing a lot of the ground work. We couldnt have done it without them.  
If you are interested in this bot you may also like to check out their projects.  
- EldenRingAI a reinforcement learning bot running on Linux and a dual PC setup. https://github.com/jameszampa/EldenRingAI  
- EldenBot a supervised learning approach that created a lot of the computer vision groundwork and has a nice video explanaition of the basics on YouTube. https://github.com/lockwo/elden_bot  
- EldenBot video explanation: https://www.youtube.com/watch?v=ViFgSxzHhRU
- Discord server for EldenBot: https://discord.gg/nThwu88Q
