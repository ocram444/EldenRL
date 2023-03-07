from stable_baselines3 import PPO, A2C
from sb3_contrib import RecurrentPPO, QRDQN
#from stable_baselines3.common.evaluation import evaluate_policy
import os
from EldenEnv import EldenEnv


#📍 To do:
#📍 #1 Tensorboard logging of avarage reward per episode to see if the model is improving


print("👵💍 EldenRL - Train.py 👵💍")
print("🧠 Hello. Training will start soon. This can take a while to initialize...")

RESUME = True			#📍 If true, the model will be loaded from the model_path and continue training from there. If false, a new model will be created.
TIMESTEPS = 1			#📍 How many times the model.learn() calles itself before the code after it is executed. With the variable being 1 the function model.save() is called after each learn() call.
HORIZON_WINDOW = 200	#📍 This is the number of steps the model will take in EldenEnv() before one model.learn() TIMESTEP is finished. The agent maybe takes ~50 steps in one death so this is ~4 deaths. ~2min


# Create log and model directories if they don't exist
#check if the path exists, if not create it 
model_name = "PPO-1" 					#📍 Creating folder structure
if not os.path.exists(f"models/{model_name}/"):
	os.makedirs(f"models/{model_name}/")
if not os.path.exists(f"logs/{model_name}/"):
	os.makedirs(f"logs/{model_name}/")
models_dir = f"models/{model_name}/"	#📍 Set the path variables
logdir = f"logs/{model_name}/"			
model_path = f"{models_dir}/PPO-1.zip" #📍 Model location and name. Use iter if you want to save multiple models with the same name.
print("🧠 Folder structure created...")


env = EldenEnv()	#📍 We initialize the custom environment for the game. Its what the agent sees, controls and gets rewarded for. This is the class we created in EldenEnv.py
print("🧠 EldenEnv initialized...")


if not RESUME:	#📍 You can resume training from a saved model. If you want to start from scratch, set RESUME to False.
	model = PPO('MultiInputPolicy',	#📍 This is the model. We are using PPO because I heared it is the best.
						env,		#📍 EldenEnv
						tensorboard_log=logdir,	#📍 Log directory
						n_steps=HORIZON_WINDOW,	#📍 When the model is updated. ~2min
						verbose=1,		#📍 Idk you never change this.
						device='cpu')	#📍 You also never change this.
	iters = 0	#📍 If you want a fancy name for the model, or maybe also save old models without overwriting them with the same name, you can add iter to the model name.
	print("🧠 New Model created...")
else:
	model = PPO.load(model_path, env=env)	#📍 Load the model from the model_path
	iters = 0 								#📍 If you want a fancy name for the model, you need to somehow get iter here and set it.
	print("🧠 Model loaded...")


while True:								#📍 This is the training loop.
	iters += 1							#📍 Iter counts the number of times the model is times the model was saved. You could use it in the model name.
	model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO", log_interval=1) #📍 This is the actual training. We dont reset the timesteps so the max timesteps is not reset on death of the agent.
	model.save(f"{models_dir}/PPO-1")	#📍 Save the model with the name PPO-1. This will overwrite the old model with the same name.
	print(f"🧠 Model saved {iters} times.")
	

