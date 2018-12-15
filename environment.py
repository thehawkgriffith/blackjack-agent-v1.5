import numpy as np
class Environment:
    
    def __init__(self):
        self.dealer_sum = 0
        self.deck = ['A', 'K', 'Q', 'J', '10', '9',
                     '8', '7', '6', '5', '4', '3', '2']
        self.player_sum = 0
        self.dealer_cards = []
        self.player_cards = []
        self.mapping = {'K':10, 'Q':10, 'J':10, '10':10, '9':9,
                     '8':8, '7':7, '6':6, '5':5, '4':4, '3':3, '2':2}
        self.first = True
        self.usable_ace = 1
        
    def compute_sum(self, cards):
        curr_sum = 0
        prev_sum = 0
        for card in cards:
            if card != 'A':
                prev_sum += self.mapping[card]
        for card in cards:
            if card == 'A':
                if prev_sum + 11 <= 21:
                    curr_sum += 11
                    self.usable_ace = 1
                else:
                    curr_sum += 1
                    self.usable_ace = 0
        return curr_sum + prev_sum
        
    def step(self, action):
        # state = [current_sum, dealer's_showing_card, usable_ace]
        if self.player_sum == 21 and self.first:
            if self.dealer_sum != 21:
                return ((21, self.dealer_cards[0], self.usable_ace), +1, True)
            self.first = False
        if action == 'H':
            self.player_cards.append(np.random.choice(self.deck))
            self.player_sum = self.compute_sum(self.player_cards)
            state = (self.player_sum, self.dealer_cards[0], self.usable_ace)
            if self.player_sum > 21:
                reward = -1
                return (state, reward, True)
            else:
                return (state, 0, False)
        if action == 'S':
            if self.compute_sum(self.dealer_cards) > 21:
                return ((self.compute_sum(self.player_cards), self.dealer_cards[0], self.usable_ace), +1, True)
            else:
                if self.compute_sum(self.dealer_cards) < 17:
                    self.dealer_cards.append(np.random.choice(self.deck))
                    k = self.step('S')
                    return k
                else:
                    if self.compute_sum(self.dealer_cards) <= 21:
                        if (21 - self.compute_sum(self.dealer_cards)) < (21 - self.compute_sum(self.player_cards)):
                            return ((self.compute_sum(self.player_cards), self.dealer_cards[0], self.usable_ace), -1, True)
                        elif (21 - self.compute_sum(self.dealer_cards)) == (21 - self.compute_sum(self.player_cards)):
                            return ((self.compute_sum(self.player_cards), self.dealer_cards[0], self.usable_ace), 0, True)
                        else:
                            return ((self.compute_sum(self.player_cards), self.dealer_cards[0], self.usable_ace), +1, True)
                    else:
                        return ((self.compute_sum(self.player_cards), self.dealer_cards[0], self.usable_ace), +1, True)

    def reset(self):
        self.dealer_cards = [np.random.choice(self.deck), np.random.choice(self.deck)]
        self.player_cards = [np.random.choice(self.deck), np.random.choice(self.deck)]
        self.dealer_sum = self.compute_sum(self.dealer_cards)
        self.player_sum = self.compute_sum(self.player_cards)
        return ((self.compute_sum(self.player_cards), self.dealer_cards[0], self.usable_ace), 0, False)
        
    def sample_state(self):
        return (np.random.randint(0, 30), np.random.choice(self.deck), np.random.choice([0, 1]))