import random
import numpy as np

def arr_to_str(arr, sep = ';'):
	res = ''
	for i in arr:
		res += str(i) + ';'
	return res

class Agent:

	def __init__(self, discount_factor = 0.3):

		self.Times_used = {}
		self.Q = {} # state-action table
		self.df = discount_factor
		self.lr = 0.3

	def generate_values(self, state):

		self.Q[arr_to_str(state)] = np.random.random_integers(0, 20, 3)
		#self.Times_used[arr_to_str(state)] = 0

	def update(self, state, action, reward):
		'''
		actions:
		0 - go forward
		1 - go left
		2 - go right
		'''

		#self.Times_used[arr_to_str(state)] += 1

		#lr = 1/self.Times_used[arr_to_str(state)] # learning rate
		lr = self.lr
		if self.lr > 0.1:
			self.lr -= 0.01

		self.Q[arr_to_str(state)][action] = (1-lr) * self.Q[arr_to_str(state)][action] + lr * (reward + self.df * self.maxQ(state))
		#print(state, ' x ', action)

	def maxQ(self, state):

		return max(self.Q[arr_to_str(state)])

	def predict(self, state):

		#print(arr_to_str(state))
		if not arr_to_str(state) in self.Q:
			self.generate_values(state)
		mx = self.Q[arr_to_str(state)][0]

		#print(self.Q)
		mxa = 0

		for i in range(len(self.Q[arr_to_str(state)])):
			if self.Q[arr_to_str(state)][i] > mx:
				mx = self.Q[arr_to_str(state)][0]
				mxa = i

		return mxa

	def save_to_file(self, path):
		f = open(path, 'w')
		for k, v in self.Q.items():
			if k == None:
				continue
			#print(k , ' ' , v)
			f.write(k + 'O' + arr_to_str(v, sep = ';') + '$')
		f.close()

	def load_from_file(self, path):
		f = open(path, 'r').read()
		states = f.split('$')
		for state in states:
			it = state.split('O')
			if len(it) < 2:
				continue
			st = it[0]
			acts = []
			for act in it[1].split(';'):
				if len(act) > 0: 
					acts.append(float(act))
			self.Q[st] = acts