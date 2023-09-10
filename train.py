from stable_baselines3 import PPO, A2C
import os
from EldenEnv import EldenEnv


def train(RESUME_TRAINING, DEBUG_MODE):
	print("🧠 Training will start soon. This can take a while to initialize...")


	TIMESTEPS = 1			#Learning rate multiplier.
	HORIZON_WINDOW = 500	#Lerning rate number of steps before updating the model. ~2min


	'''Creating folder structure'''
	model_name = "PPO-1" 					
	if not os.path.exists(f"models/{model_name}/"):
		os.makedirs(f"models/{model_name}/")
	if not os.path.exists(f"logs/{model_name}/"):
		os.makedirs(f"logs/{model_name}/")
	models_dir = f"models/{model_name}/"
	logdir = f"logs/{model_name}/"			
	model_path = f"{models_dir}/PPO-1.zip"
	print("🧠 Folder structure created...")


	'''Initializing environment'''
	env = EldenEnv()
	print("🧠 EldenEnv initialized...")


	'''Creating new model or loading existing model'''
	if not RESUME_TRAINING:
		model = PPO('MultiInputPolicy',
							env,
							tensorboard_log=logdir,
							n_steps=HORIZON_WINDOW,
							verbose=1,
							device='cpu')	#Set training device here.
		print("🧠 New Model created...")
	else:
		model = PPO.load(model_path, env=env)
		print("🧠 Model loaded...")


	'''Training loop'''
	while True:
		model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO", log_interval=1)
		model.save(f"{models_dir}/PPO-1")
		print(f"🧠 Model updated...")
		

