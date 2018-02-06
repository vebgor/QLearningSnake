import curses
import pygame
import random
import sys
from time import time
import numpy as np
import getch
from agent import Agent
import math

# get mode
args = sys.argv
# 0 - train, 1 - test
mode = 'play'

path = '/Users/egorbalzin/Documents/ZPD/table.Qtable'
training_data_path = '/Users/egorbalzin/Documents/ZPD/training_data.txt'
test_data_path = '/Users/egorbalzin/Documents/ZPD/test_data.txt'

if len(args) >= 2:
	mode = args[1]

	if mode != 'test' and mode != 'train' and mode != 'play':
		print('wrong input')
		exit()
print(mode)
# constants

UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)

screenX = 500
screenY = 500
fieldX = 20
fieldY = 20
sqX = screenX / fieldX
sqY = screenY / fieldY

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

train_moves = 10**6

# snake

class Snake:

	def __init__(self, pos = (0, 0), dir = DOWN):
		self.body = [pos]
		self.direction = dir
		self.to_grow = False

	def step(self):
		next_pos = self.get_next_pos()
		self.body = [next_pos] + self.body

		if self.to_grow:
			self.to_grow = False
		else:
			self.body.pop()

	def get_next_pos(self):
		next_pos = self.body[0]
		next_pos = (next_pos[0] + self.direction[0], next_pos[1] + self.direction[1])
		return next_pos

	def turn_left(self):
		self.direction = (self.direction[1], self.direction[0] * -1)

	def turn_right(self):
		self.direction = (self.direction[1] * -1, self.direction[0])

	def grow(self):
		self.to_grow = True

	def draw(self):

		global field

		age = len(self.body)
		for pos in self.body:
			field[pos[1]][pos[0]] = age
			age = age - 1

	def get_state1(self, apple):

		global field 

		res = [0] * 5
		p = self.body[0]
		x = apple[0] - p[0]
		y = apple[1] - p[1]

		if self.direction == UP:
			res[0] = -x
			res[1] = -y
		if self.direction == RIGHT:
			res[0] = -y
			res[1] = x
		if self.direction == LEFT:
			res[0] = y
			res[1] = -x
		if self.direction == DOWN:
			res[0] = x
			res[1] = y

		npos = self.get_next_pos()
		if field[npos[1]][npos[0]] > 1:
			res[2] = 1
		self.turn_left()
		npos = self.get_next_pos()
		if field[npos[1]][npos[0]] > 1:
			res[3] = 1
		self.turn_right()
		self.turn_right()
		if field[npos[1]][npos[0]] > 1:
			res[4] = 1
		self.turn_left()

		return res



# drawing functions

def init_graphics():
	'''global screen

	pygame.init()
	screen = pygame.display.set_mode((screenX, screenY))
	'''
	return

def draw_field():
	'''
	global screen
	global field

	screen.fill(BLACK)

	y = 0
	for line in field:
		x = 0
		for cell in line:
			color = WHITE
			if cell > 0:
				color = GREEN
			if cell < 0:
				color = RED

			pygame.draw.rect(screen, color, pygame.Rect(x * sqX + 2, y * sqY + 2, sqX - 4, sqY - 4))

			x += 1
		y += 1

	pygame.display.flip()
	'''

	'''
	for line in field:
		print(line)
	'''
	return
	

def get_pressed_buttons():
	btns = []
	'''
	for event in pygame.event.get():

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				btns.append('l')
			if event.key == pygame.K_RIGHT:
				btns.append('r')
	'''

	key = getch.getch()

	if key == 'a':
		btns.append('l')
	if key == 'd':
		btns.append('r')

	return btns

# nn functions

def load_table():
	return 

def save_table():

	global agent
	agent.save_to_file(path)

	return

# helper functions
def clear_field():
	global field

	field = [0] * fieldY

	for i in range(fieldY):
		field[i] = [0] * fieldX
	
	for i in range(fieldX):
		field[0][i] = field[fieldX-1][i] =  401

	for i in range(fieldY):
		field[i][0] = field[i][fieldY-1] = 401

def dist(head, apple):
	return abs(head[0]-apple[0])+abs(head[1]- apple[1])

# game

all_step_count = 0

def new_game(): 

	global all_step_count
	global agent

	snake = Snake(pos = (5, 5))

	if mode != 'train':
		init_graphics()

	done = False


	clear_field()

	apple = (12, 14)

	t = time()
	btns = []

	step_count = 0
	score = 0
	distance = dist(snake.body[0], apple)

	t = time()
	while not done:

		#if mode == 'test':
			#draw_field()

		reward = -10
		ate = False
		step_count += 1
		all_step_count += 1

		if (all_step_count > train_moves and mode != 'test') or (((step_count > 1000 and step_count/max(1, score) > 1000) or (all_step_count > 100000)) and mode == 'test'):
			return step_count, score

		if all_step_count % 10000 == 0:
			print(all_step_count)

		state = snake.get_state1(apple)
		#print(state)
		#print(state)
		act = 0
		if mode == 'play':
			btns = btns + get_pressed_buttons()
		else:
			act = agent.predict(state)
			if act == 1: 
				btns = ['l']
			if act == 2:
				btns = ['r']



		for btn in btns:
			if btn == 'l':
				snake.turn_left()
			if btn == 'r':
				snake.turn_right()

		btns = []
		(X, Y) = snake.get_next_pos()

		#print(X, Y)
		#print('apple:', apple)
		if field[Y][X] < 0:
			snake.grow()
			ate = True
			score += 1
			reward = 500


		if field[Y][X] > 1:
			done = True
			if mode == 'play':
				pygame.quit()
				exit()
			if mode == 'train':
				reward = -100
				agent.update(state, act, reward)
				return step_count, score
			if mode == 'test':
				return step_count, score


		clear_field()

		snake.step()


		new_dist = dist(snake.body[0], apple)
		if new_dist < distance:
			reward = max(reward, 100)
		distance = new_dist

		snake.draw()

		if ate:
			while field[apple[1]][apple[0]] != 0:
				apple = (random.randint(0, fieldX - 1), random.randint(0, fieldY-1))


		field[apple[1]][apple[0]] = -1

		if mode == 'play':
			draw_field()

		if mode == 'train':
			agent.update(state, act, reward)

		


if mode == 'play':
	new_game()
elif mode == 'train':
	global agent

	agent = Agent()

	avgS = 0
	avgSc = 0
	gm = 0
	highscore = 0
	while all_step_count < train_moves:
		steps, score = new_game()
		gm += 1
		avgS += steps
		avgSc += score 
		if score > highscore:
			highscore = score

	avgS /= gm
	avgSc /= gm
	f = open(training_data_path, 'w')
	f.write('average step amount: ' + str(avgS) + ' average score: ' + str(avgSc) + ' highscore: ' + str(highscore))
	f.close()

	save_table()

elif mode == 'test':
	#global agent

	agent = Agent()
	agent.load_from_file(path)
	
	avgS = 0
	avgSc = 0
	gm = 0
	highscore = 0
	for _ in range(100):
		steps, score = new_game()
		print(score, ' ', highscore)
		gm += 1
		avgS += steps
		avgSc += score 
		if score > highscore:
			highscore = score

	avgS /= gm
	avgSc /= gm

	f = open(test_data_path, 'w')
	f.write('average step amount: ' + str(avgS) + ' average score: ' + str(avgSc) + ' highscore: ' + str(highscore))
	f.close()

