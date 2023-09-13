# EldenRL - Elden Ring Ai
Reinforcement Learning for Elden Ring on Windows11.  
  
The goal of this project is to create a basic working version of a reinforcement learning agent for Elden Ring. The agent should be able to fight all bosses if trained long enough on them.

![Component 1](https://github.com/ocram444/EldenRL/assets/113638653/4a6ce798-4797-43a1-a48c-1ed20cf88d12)

# Description
***<b>The Readme is pretty outdated</b>***<br>
This project uses a custom OpenAI gym environment that feeds the agent a picture of the game, previous actions, and health. The agent then decides an action to take and is rewarded based on damage delt to the boss, damage taken and some other rewards. For now only bosses behind fog gates (no open world bosses) are implemented but it shouldnt be too hard to adjust the code for open world bosses too.  
It is programmed with modularity in mind. It should be fairly easy to hook in other actions, observations, rewards or any other functions you may want.  
Learning and decision making is completely handled by Stable-Baselines3 using PPO and the custom environment.  
The code is written 100% in python for Windows11.  
It runs at ~2.4fps on my i9 13900k CPU with the game running normally on my GPU.  

# Other
- You should probably launch Elden Ring in offline mode if you dont want to end up getting banned from online play. I am not doing that and I havent been banned yet though...  
- Letting the Ai fight/train in pvp matches is probably not happening any time soon. But it could be possible...  
- Fighting groups of enemies / non boss encounters in the open world is also something I would like to see. But nothing has been done for that yet. 
- Walking to the boss/fog gate is hard coded for every boss. I kind of want to create a seperate Ai that navigates the open world but I cant really think of any way to achieve that yet...
- I'll be working more on this project with Twitch integration and some extra stuff. I do not expect that I will be pushing that to this depository. This is purely the bot that plays/trains fighting Elden Ring bosses.  
- You may use this for any of your own projects. Again, it should be fairly easy to expand on the functionality.  
- I cant upload my basic trained model to GitHub because it is too big a file. Please train your own by setting RESUME = False in train.py

# Videos<br>
EldenRL PvE showcase: https://www.youtube.com/watch?v=NzTwDO4ehPY<br>
EldenRL PvP showcase: https://www.youtube.com/watch?v=2Uh1T8FE0y8


# Credits
Huge shoutout to Jameszampa and Lockwo for doing a lot of the ground work. I couldnt have done it without them.  
If you are interested in this bot you may also like to check out their projects.  
- EldenRingAI a reinforcement learning bot running on Linux and a dual PC setup. https://github.com/jameszampa/EldenRingAI  
- EldenBot a supervised learning approach that created a lot of the computer vision groundwork and has a nice video explanaition of the basics on YouTube. https://github.com/lockwo/elden_bot  
- EldenBot video explanation: https://www.youtube.com/watch?v=ViFgSxzHhRU
- Discord server for EldenBot: https://discord.com/channels/984553640071155752/984553641815982140
