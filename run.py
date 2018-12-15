import numpy as np
import matplotlib.pyplot as plt
from environment import Environment
from agent import Agent

def render(env, action):
    print("-------------------------------")
    print("Current Hands are:-")
    print("Dealer has the following cards:")
    print("{} and []".format(env.dealer_cards[0]))
    print("Agent has the following cards:")
    print(env.player_cards)
    if action == 'H':
        print("Agent chooses to hit.")
    else:
        print("Agent chooses to stay.")

def play_a_hand(env, agent, ren=False):
    if ren == True:
    	s, r, done = env.reset()
    	while not done:
        	a = agent.take_action(s)
        	render(env, a)
        	sp, r, done = env.step(a)
        	s = sp
    	print("After Dealer's play...\nDealer has:")
    	print(env.dealer_cards)
    	if r == 1:
        	print("Agent won the hand.")
    	elif r==-1:
        	print("Agent lost the hand.")
    	else:
        	print("It's a draw.")
    else:
    	s, r, done = env.reset()
    	while not done:
        	a = agent.take_action(s)
        	sp, r, done = env.step(a)
        	s = sp
    return r


env = Environment()
agent = Agent(env)
agent.train(env)
agent.train_mode = False
running_avg = []
for _ in range(100):
    rewards = []
    for _ in range(1000):
        r = play_a_hand(env, agent)
        #if r == -1: ## To see what is it's sole probability to win
        #	r = 0
        rewards.append(r)
    running_avg.append(np.mean(rewards))
plt.plot(running_avg)
plt.show()
print("Average reward attained is: ", np.mean(running_avg))
play_a_hand(env, agent, True)
#agent.print_policy(env)