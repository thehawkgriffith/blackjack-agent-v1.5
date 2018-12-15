import numpy as np

class Agent:
    
    def __init__(self, env):
        self.train_mode = True
        self.states = set()
        self.actions = ['H', 'S']
        for _ in range(100000):
            self.states.add(env.sample_state())
        self.states = list(self.states)
        self.Q = {}
        self.policy = {}
        for state in self.states:
            self.Q[state] = {}
            for action in self.actions:
                self.Q[state][action] = np.random.random()
        for state in list(self.Q.keys()):
            if self.Q[state]['H'] > self.Q[state]['S']:
                self.policy[state] = 'H'
            else:
                self.policy[state] = 'S'

    def take_action(self, state, eps=0.05):
        if self.train_mode:
            if np.random.random() > eps:
                return self.policy[state]
            else:
                return np.random.choice(['H', 'S'])
        else:
            return self.policy[state]
            
    def train(self, env, epochs=10000, eps=0.05):
        returns = {}
        for state in self.states:
            returns[state] = {}
            for action in self.actions:
                returns[state][action] = []
        for _ in range(epochs):
            episode = []
            seen_states = set()
            s, r, done = env.reset()
            while not done:
                a = self.take_action(s, eps)
                sp, r, done = env.step(a)
                episode.append((s, a, r))
                s = sp
            G = 0
            for step in reversed(episode):
                s, a, r = step
                G = 0.9*G + r  
                if (s, a) not in seen_states:
                    seen_states.add((s, a))
                    returns[s][a].append(G)
                    self.Q[s][a] = np.mean(returns[s][a])
                    self.gen_optimum_policy()
    
    def gen_optimum_policy(self):
        for state in list(self.Q.keys()):
            if self.Q[state]['H'] > self.Q[state]['S']:
                self.policy[state] = 'H'
            else:
                self.policy[state] = 'S'

    def print_policy(self, env):
        print("Policy is: ")
        count = 40
        seen_states = {}
        for state in self.states:
            seen_states[state] = 0
        for _ in range(10000):
            s, r, done = env.reset()
            while not done:
                a = self.take_action(s)
                sp, r, done = env.step(a) 
                seen_states[s] += 1
                s = sp
        neo_policy = {}
        for state in self.states:
            if seen_states[state] > count:
                neo_policy[state] = self.policy[state]
        for state in neo_policy:
            print("Sum of player's cards: {}\nDealer's Card: {}\nAction: {}".format(state[0], state[1], neo_policy[state]))