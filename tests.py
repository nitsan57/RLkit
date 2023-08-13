from Agents.explorers import RandomExplorer
from Agents.agent_utils import ObsWraper
from Models import fc, rnn
from Agents.dqn_agent import DQN_Agent
from Agents.ppo_agent import PPO_Agent
import numpy as np
import torch
from tqdm import tqdm
import utils
import gymnasium as gym


# def unittest():
#     """Not implemnted yet"""
#     ObsWraper(np.zeros((3,3))).shape
#     obs = ObsWraper(
#         {'data': 3}
#     )
#     obs2 = ObsWraper(
#         {'data': 4}
#     )
#     obs3 = ObsWraper(
#         {'data': 5}
#     )
#     obs_list = [obs, obs2, obs3]
#     ObsWraper(obs_list).shape
#     import torch

#     obs = ObsWraper(
#         {'data': torch.tensor(3)}
#     )
#     obs2 = ObsWraper(
#         {'data': torch.tensor(4)}
#     )
#     obs3 = ObsWraper(
#         {'data': torch.tensor(5)}
#     )
#     obs_list = [obs, obs2, obs3]
#     ObsWraper(obs_list)


def run_for_d(a, e_name):
    env_c2 = gym.make(e_name, render_mode=None)
    reward = a.run_env(env_c2, render=True, best_act=True)
    print("Run Reward:", reward)
    import pygame
    pygame.display.quit()


def test_2e2():
    device = utils.init_torch('cuda')
    #  PPO DQN CONT DISC MULTI-ACTIONS CONT RNN
    # TEST DISCRETE
    # +PPO
    # ++FC
    env = gym.make("LunarLander-v2", render_mode=None)
    model_class = fc.FC
    model_kwargs = {'embed_dim': 64, 'repeat':2}
    agent = PPO_Agent(obs_space=env.observation_space, action_space=env.action_space, device=device, batch_size=1024, max_mem_size=10**5, num_parallel_envs=4, lr=3e-4, entropy_coeff=0.05, model_class=model_class, model_kwargs=model_kwargs, discount_factor=0.99)
    train_stats = agent.train_n_steps(env=env,n_steps=10000)
    # ++RNN
    env_name = "LunarLander-v2"
    env = gym.make(env_name, render_mode=None, continuous=True)
    model_class_c = rnn.GRU
    model_kwargs_c = {} #{'embed_dim': 64, 'repeat':2}
    agent_c = PPO_Agent(obs_space=env.observation_space, action_space=env.action_space, device=device, batch_size=1024, max_mem_size=10**5, num_parallel_envs=4, lr=3e-4, entropy_coeff=0.05, model_class=model_class_c, model_kwargs=model_kwargs_c, discount_factor=0.99,kl_div_thresh=0.05, clip_param=0.3)
    train_stats_C = agent_c.train_n_steps(env=env,n_steps=1000)
    #DQN
    # ++FC
    env_name = "CartPole-v1"
    env_c = gym.make(env_name, render_mode=None)
    model_class_c = fc.FC
    model_kwargs_c = {'embed_dim': 64, 'repeat':2}
    agent_c = DQN_Agent(obs_space=env_c.observation_space, action_space=env_c.action_space, batch_size=16, max_mem_size=10**5,num_parallel_envs=16, lr=1e-3,  model_class=model_class_c, model_kwargs=model_kwargs_c, discount_factor=0.99, explorer = RandomExplorer(1,0.05,0.01), target_update_time=100)
    train_stats_c = agent_c.train_episodial(env=env_c,n_episodes=32)
    # ++RNN
    env_name = "Taxi-v3"
    env_c = gym.make(env_name, render_mode=None)
    model_class_c = rnn.GRU
    model_kwargs_c = {'hidden_dim': 64, 'num_grus':2}
    agent_c = DQN_Agent(obs_space=env_c.observation_space, action_space=env_c.action_space, batch_size=16, max_mem_size=10**5,num_parallel_envs=16, lr=1e-3,  model_class=model_class_c, model_kwargs=model_kwargs_c, discount_factor=0.99, explorer = RandomExplorer(1,0.05,0.01), target_update_time=100)
    train_stats_c = agent_c.train_episodial(env=env_c,n_episodes=32)


    # TEST CONT
    # +PPO
    # ++FC
    car_env = gym.make("MountainCarContinuous-v0", render_mode=None)
    agent_car = PPO_Agent(obs_space=car_env.observation_space, action_space=car_env.action_space, device=device, batch_size=4096, max_mem_size=10**5,num_parallel_envs=4, lr=3e-4, model_class=fc.FC, explorer = RandomExplorer(0.3,0,0))
    train_stats_c = agent_car.train_n_steps(env=car_env,n_steps=1000)
    # ++RNN, (MULTI-ACTIONS)
    env_name = "LunarLanderContinuous-v2"
    env = gym.make(env_name, render_mode=None, continuous=True)
    model_class_c = rnn.GRU
    model_kwargs_c = {} #{'embed_dim': 64, 'repeat':2}
    agent_c = PPO_Agent(obs_space=env.observation_space, action_space=env.action_space, device=device, batch_size=1024, max_mem_size=10**5, num_parallel_envs=4, lr=3e-4, entropy_coeff=0.05, model_class=model_class_c, model_kwargs=model_kwargs_c, discount_factor=0.99,kl_div_thresh=0.05, clip_param=0.3)
    train_stats_C = agent_c.train_n_steps(env=env,n_steps=1000)
    # +DQN - NOT SUPPORTED CURRENTLY
    # ++FC
    # ++RNN
    # TEST FUNCNIONALITY, (MULTI-ACTIONS)
    car_env = gym.make("LunarLanderContinuous-v2", render_mode=None)
    agent_car = PPO_Agent(obs_space=car_env.observation_space, action_space=car_env.action_space, device=device, batch_size=4096, max_mem_size=10**5,num_parallel_envs=4, lr=3e-4, model_class=fc.FC, explorer = RandomExplorer(0.3,0,0))
    train_stats_c = agent_car.train_n_steps(env=car_env,n_steps=1000)
    _ = agent_car.save_agent("/tmp/TEMP.pt")
    agent_car.load_agent("/tmp/TEMP.pt")


def main():
    test_2e2()




if __name__ == "__main__":
    main()