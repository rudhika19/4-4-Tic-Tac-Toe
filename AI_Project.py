# -*- coding: utf-8 -*-
import copy
import datetime
import numpy as np
import sys
import random
from Tkinter import Tk, Button
from tkFont import Font


# Defining minimum utility and maximum utility values as -1000 and 1000 respectively
min_utility = -1000
max_utility = 1000

# Defining Human player to be O and Computer Player to be X
min_player = 'O'
max_player = 'X'

make_move = 1


# The class board contains the logic of the game 
class Board:
	maximum_depth = 0
	cuttoff_occured = 0
	total_nodes = 0
	max_pruning = 0
	min_pruning = 0

# Successors function is used to generate all the successors from the current state of the board
# It accepts two parameters : player i.e the Current Player for which all possible moves needs to be generated and 
# board which is the current configuration of the board 
	def successors(self,player,board):
		successors_list = []
		i,j =0,0
# This produces all possible moves for player X by replacing all empty boxes with X one by one and stores them in a list : successors_list
		if player == 'X':
			while i< 4:
				j =0
				while j < 4:
					temp_board = copy.deepcopy(board)
					if (temp_board[i][j]=='_'):
						temp_board[i][j] = 'X'
						successors_list.append(temp_board)
					j += 1
				i += 1
		i,j = 0,0
# This produces all possible moves for player O by replacing all empty boxes with O one by one and stores them in a list : successors_list
		if player == 'O':
			while i< 4:
				j =0
				while j < 4:
					temp_board = copy.deepcopy(board)
					if (temp_board[i][j]=='_'):
						temp_board[i][j] = 'O'
						successors_list.append(temp_board)
					j += 1
				i += 1
# The function returns the list of all possible successors
		return successors_list


# This function prints the 2d list board in a presentable board format
	def printboard(self,board):
		for i in board:
			for j in i:
				print j+" ",
			print ""

# This function computes both the evaluation function and the final utility values 
	def evaluation(self,board):
# Eval(s)= 6X3 + 3X2 + X1 − (6O3 + 3O2 + O1)
# The x_array contains X1, X2, X3, X4 in this order
# The o_array contains 01, 02, 03, 04 in this order
		x_array = [0,0,0,0]
		o_array = [0,0,0,0]
		i,j,nx,no = 0,0,0,0
# This loop basically iterates on every row and stores the total no of x's and o's in variables
# counter counts total no of xs and os which is used later to determine if a draw has occured 
		counter = 0
		while i < 4: 
			j,nx,no = 0,0,0
			while j < 4:
				if board[i][j] == 'X':
					nx = nx+1
					counter+=1
				if board[i][j] == 'O':
					no = no+1
					counter+=1
				j+=1
# If any row contains no x's and only o's we increment the counter of O(n) where n is the number of o's
			if(nx==0 and no!=0):
				o_array[no-1] += 1
# If any row contains no o's and only x's we increment the counter of X(n) where n is the number of x's
			if(no==0 and nx!=0):
				x_array[nx-1] += 1  
			i+=1
		i,j,nx,no = 0,0,0,0
# This loop iterates on columns and does the same thing as the previous loop
		for i in zip(*board):
			nx = 0
			no = 0
			for j in i:
				if j == 'X':
					nx = nx + 1
				if j == 'O':
					no = no + 1
			if(nx==0 and no!=0):
				o_array[no-1] += 1
			if(no==0 and nx!=0):
				x_array[nx-1] += 1 
# This loop checks for diagnol 45 and increments X(n) or O(n) or none 
		i,j,nx,no = 0,0,0,0
		while i < 4: 
			j = 0 
			while j < 4:
				if i == j:
					if board[i][j] == 'X':
						nx = nx+1
					if board[i][j] == 'O':
						no = no+1
				j+=1
			i+=1
		if(nx==0 and no!=0):
			o_array[no-1] += 1
		if(no==0 and nx!=0):
			x_array[nx-1] += 1  
# This loop checks for diagnol 135 and increments X(n) or O(n) or none 
		i,j,nx,no = 0,0,0,0
		while i < 4: 
			j = 0 
			while j < 4:
				if i == 3 - j:
					if board[i][j] == 'X':
						nx = nx+1
					if board[i][j] == 'O':
						no = no+1
				j+=1
			i+=1
		if(nx==0 and no!=0):
			o_array[no-1] += 1
		if(no==0 and nx!=0):
			x_array[nx-1] += 1  

# This part determines if either x has won (by checking if it has four in a line somewhere) or o has won or its a draw and returns the correspondind
# utilty values as the second returned value and the first returned value being 1 indicating the game is over
		if x_array[3] == 1:
			return 1,1000
		if o_array[3] == 1:
			return 1,-1000  
		if counter == 16:
			return 1,0
# Here we return the evaluation function score using all the values we updated earlier
		score = 6*(x_array[2]-o_array[2])+3*(x_array[1]-o_array[1])+(x_array[0]-o_array[0])
# We return 0 as first value to indicate that this is the evaluation score 
		return 0,score


# This function is used to calculate the evaluation function for the intermediate level of the game 
# The function used is Number of remaining ways (rows, columns or diagonals which can still be filled to winning state) to win for x - Number of remaining ways to win for 0
# The variables x_points and o_points are used to store no of colums diagnols or rows (including empty ones) where x and o still have a chance of winning 
	def evaluation_medium(self,board):
		x_array = [0,0,0,0]
		o_array = [0,0,0,0]
		i,j,nx,no = 0,0,0,0
		x_points = 0
		o_points = 0
# This loop iterates on all the rows and increments x_points and o_points for rows 
		counter = 0
		while i < 4: 
			j,nx,no = 0,0,0
			while j < 4:
				if board[i][j] == 'X':
					nx = nx+1
					counter+=1
				if board[i][j] == 'O':
					no = no+1
					counter+=1
				j+=1
			#print nx,no
			if(nx==0 and no!=0):
				o_array[no-1] += 1
				o_points +=1
			if(no==0 and nx!=0):
				x_array[nx-1] += 1  
				x_points +=1
			if(no==0 and nx==0):
				x_points+=1
				o_points +=1
			i+=1
		i,j,nx,no = 0,0,0,0

# This loop iterates on all the columns and increments x_points and o_points for columns
		for i in zip(*board):
			nx = 0
			no = 0
			for j in i:
				if j == 'X':
					nx = nx + 1
				if j == 'O':
					no = no + 1
			if(nx==0 and no!=0):
				o_array[no-1] += 1
				o_points +=1
			if(no==0 and nx!=0):
				x_array[nx-1] += 1
				x_points +=1 
			if(no==0 and nx==0):
				x_points+=1
				o_points +=1

# This loop iterates on the 45 degree diagno  and increments x_points and o_points for it if valid
		i,j,nx,no = 0,0,0,0
		while i < 4: 
			j = 0 
			while j < 4:
				if i == j:
					if board[i][j] == 'X':
						nx = nx+1
					if board[i][j] == 'O':
						no = no+1
				j+=1
			i+=1
		if(nx==0 and no!=0):
			o_array[no-1] += 1
			o_points +=1
		if(no==0 and nx!=0):
			x_array[nx-1] += 1  
			x_points +=1
		if(no==0 and nx==0):
			x_points+=1
			o_points +=1

# This loop iterates on the 135 degree diagno  and increments x_points and o_points for it if valid
		i,j,nx,no = 0,0,0,0
		while i < 4: 
			j = 0 
			while j < 4:
				if i == 3 - j:
					if board[i][j] == 'X':
						nx = nx+1
					if board[i][j] == 'O':
						no = no+1
				j+=1
			i+=1
		if(nx==0 and no!=0):
			o_array[no-1] += 1
			o_points += 1
		if(no==0 and nx!=0):
			x_array[nx-1] += 1  
			x_points +=1
		if(no==0 and nx==0):
			x_points+=1
			o_points +=1

# This part determines if either x has won (by checking if it has four in a line somewhere) or o has won or its a draw and returns the correspondind
# utilty values as the second returned value and the first returned value being 1 indicating the game is over
		if x_array[3] == 1:
			return 1,1000
		if o_array[3] == 1:
			return 1,-1000  
		if counter == 16:
			return 1,0

# Here we return the evaluation function score using all the values we updated earlier
		score = x_points - o_points
		return 0,score

	def alpha_beta_search(self,board,difficulty_level):
		global min_pruning
		min_pruning = 0
		global max_pruning
		max_pruning = 0
		global total_nodes
		total_nodes = 0
		global maximum_depth
		maximum_depth = 0
		global cuttoff_occured
		cuttoff_occured = 0

# Created a date time object to determine the time at the start of the alpha beta search algorithm 
		start_time = datetime.datetime.now()
		depth = 0
# Calling the max value function which returs the next move to be played and its utility value 
		v,returnstate = self.max_value(board,min_utility,max_utility,start_time,depth,difficulty_level)

# Printing STATISTICS of the game as mentioned in the question
		print "STATISTICS :"
		if cuttoff_occured:
			print "cuttoff occured"
		else:
			print "cuttoff did not occur"
		print "maximum depth : " + str(maximum_depth)
		print "Total number of nodes generated : " + str(total_nodes)
		print "Total number of pruning occured in max value function : " + str(max_pruning)
		print "Total number of pruning occured in min value function : " + str(min_pruning)
# Returning the next move state and its utility value 
		return v, returnstate


# Defining the max value function
	def max_value(self,board, alpha, beta, start_time,depth,difficulty_level):
		returnstate = copy.deepcopy(board)

		depth = depth + 1
		global maximum_depth 
		maximum_depth = depth
# now stores the time right now
		now = datetime.datetime.now()
# Calling evaluation functions as per the difficulty level
		if difficulty_level == 3:
			over , score = self.evaluation(board)
		if difficulty_level == 2:
			over , score = self.evaluation_medium(board)
# If the game is over at the particular board configuartion now we return the board and its utility value 
		if over == 1:
			return score,board
# Calculating time difference from start of alpha beta and now
		delta = (now - start_time)

# This condition returns the current state of the board if either the time elapsed has become greater than 10 seconds or the depth limit has exceeded 6
		if depth == 6 or delta.seconds >= 10:
			global cuttoff_occured
			cuttoff_occured = 1
			print depth
			return score,board

		v = min_utility
# Generating all successors of the current board configuration
		successors_list = self.successors('X',board)
		global total_nodes
		total_nodes = total_nodes + len(successors_list)
# Iterating on all successors of the current board
		for state in successors_list:
# Calling the min value function on each state
			minval,minstate = self.min_value(state,alpha,beta,start_time,depth,difficulty_level)
# Updating v with maximum value of the boards returned from the level below
			if v <= minval:
				v = minval
				returnstate = copy.deepcopy(state)
# Pruning branches
			if v > beta :
				global max_pruning
				max_pruning = max_pruning + 1
				return v,returnstate
# Updating the value of alpha 
			if v > alpha:
				alpha = v
# Returning best move and its utility
		return v,returnstate

# Defining the min value function
	def min_value(self,board,alpha,beta,start_time,depth,difficulty_level):
		returnstate = copy.deepcopy(board)
		depth= depth+1
		global maximum_depth 
		maximum_depth = depth

# now stores the time right now
		now = datetime.datetime.now()

# Calling evaluation functions as per the difficulty level
		if difficulty_level == 3:
			over , score = self.evaluation(board)
		if difficulty_level == 2:
			over , score = self.evaluation_medium(board)
# If the game is over at the particular board configuartion now we return the board and its utility value 
		if over == 1:
			return score,board
# Calculating time difference from start of alpha beta and now
		delta = (now - start_time)

# This condition returns the current state of the board if either the time elapsed has become greater than 10 seconds or the depth limit has exceeded 6
		if depth == 6 or delta.seconds >= 10:
			global cuttoff_occured
			cuttoff_occured = 1
			return score,board

		v = max_utility
# Generating all successors of the current board configuration
		successors_list = self.successors('O',board)
		global total_nodes
		total_nodes = total_nodes + len(successors_list)
# Iterating on all successors of the current board
		for state in successors_list:
# Calling the max value function on each state
			maxval,maxstate = self.max_value(state,alpha,beta,start_time,depth,difficulty_level)
# Updating v with minimum value of the boards returned from the level below
			if v >= maxval:
				v = maxval
				returnstate = copy.deepcopy(state)
# Pruning branches
			if v < alpha:
				global min_pruning
				min_pruning = min_pruning + 1
				return v,returnstate
# Updating the value of alpha
			if v < beta:
				beta = v
# Returning best move and its utility
		return v,returnstate

# This function determines if the game has been won by any player 
	def won(self,temp_board):
# Iterating over rows
	    x_count,o_count = 0,0
	    over =0
	    for i in temp_board:
	        x_count,o_count = 0,0
	        for j in i:
	            if j == 'X':
	                x_count=x_count+1
	            if j == 'O':
	                o_count = o_count+1
	        if x_count == 4 or o_count == 4:
	            over = 1 
	            break

# Iterating over columns
	    for i in zip(*temp_board):
	        x_count,o_count = 0,0
	        for j in i:
	            if j == 'X':
	                x_count =x_count+1
	            if j == 'O':
	                o_count = o_count + 1
	        if x_count == 4 or o_count == 4:
	            over = 1 
	            break
# Checking the diagnols 
	    if temp_board[0][0] == temp_board[1][1] == temp_board[2][2] == temp_board[3][3] == 'X':
	        over = 1
	    if temp_board[0][0] == temp_board[1][1] == temp_board[2][2] == temp_board[3][3] == 'O':
	        over = 1
	    if temp_board[0][3] == temp_board[1][2] == temp_board[2][1] == temp_board[3][0] == 'X':
	        over = 1
	    if temp_board[0][3] == temp_board[1][2] == temp_board[2][1] == temp_board[3][0] == 'O':
	        over = 1 
	    return over 

# This function initializes the board 
	def __init__(self,first,other=None):
# PLayer is set to O if it has the first move and opponent as X
		self.player = 'O'
		self.opponent = 'X'
		self.empty = '.'
		self.size = 4
		self.fields = {}
# Initially all squares are initialized as empty
		for y in range(self.size):
			for x in range(self.size):
				self.fields[x,y] = self.empty
# Temp board is also initialized and is used in the logic functions as opposeed to the board that is used for the GUI
		self.temp_board = [['_' for i in range(4)] for j in range(4)]
# If the first player is computer X is the current player and O is the opponent 
		if first == 0:
			self.player = 'X'
			self.opponent = 'O'

# This function takes the move as x,y coordinates and sets it on the board
	def move(self,board,x,y):
	
		board.fields[x,y] = board.player
		self.temp_board[y][x] = board.player
# Changes the next player 
		board.player,board.opponent = board.opponent,board.player
		return board

# This function is called to determine the move played by the computer by calling the alpha beta search algorithm 
	def move2(self):
# Parameter 3 is the difficulty level and the corresponding evaluation function is called 
		v,returnstate = self.alpha_beta_search(self.temp_board,3)
		done = 0
# Determines the x and y move from the board configuartion by comparing it to the previous board 
		for x,(i,j) in enumerate(zip(self.temp_board,returnstate)):
			if done == 1:
				break
			for y, (k,l) in enumerate(zip(i,j)):
				if k!=l:
					x1,y1= x,y
					done = 1
					break

		self.temp_board = returnstate
		self.printboard(self.temp_board)
		over = self.won(self.temp_board)
		if over == 1:
			return x1,y1,0,v
		return x1,y1,1,v

# This function is called to determine the move played by the computer by calling the alpha beta search algorithm for the intermediate level
	def move2_medium(self):
# Parameter 2 is the difficulty level and the corresponding evaluation function is called 
		v,returnstate = self.alpha_beta_search(self.temp_board,2)
		done = 0
# Determines the x and y move from the board configuartion by comparing it to the previous board 
		for x,(i,j) in enumerate(zip(self.temp_board,returnstate)):
			if done == 1:
				break
			for y, (k,l) in enumerate(zip(i,j)):
				if k!=l:
					x1,y1= x,y
					done = 1
					break

		self.temp_board = returnstate
		self.printboard(self.temp_board)
		over = self.won(self.temp_board)
		if over == 1:
			return x1,y1,0,v
		return x1,y1,1,v
# This function is called to determine the move played by the computer by calling the alpha beta search algorithm for the easy level
	def move2_easy(self):
# A random successor from all the possible successors is chosen as the move to be played  
# The easy level just generates random moves 
		successors_list = self.successors('X',self.temp_board)
		returnstate = random.choice(successors_list)
# v is assigned a random value as it has to be returned but is not required anywhere 
		v = 5
		done = 0
# Calculating the x,y position
		for x,(i,j) in enumerate(zip(self.temp_board,returnstate)):
			if done == 1:
				break
			for y, (k,l) in enumerate(zip(i,j)):
				if k!=l:
					#print x,y
					x1,y1= x,y
					done = 1
					break

		self.temp_board = returnstate
		over = self.won(self.temp_board)
		if over == 1:
			return x1,y1,0,v
		return x1,y1,1,v

# This class is designed for making the gui of the game which is a 4*4 board with clickable squares for the player to make moves 	
class GUI:

	def __init__(self):
# Getting the difficulty level and user choice as to who makes the move first from the command line
		difficulty_level = int(raw_input("Enter Level of Difficulty : 1 for Easy, 2 for Intermediate, 3 for Difficult \n"))
		first = int(raw_input("Enter which player plays first :1 for you to play first and 0 for the computer to play first"))

# An instance of the gui gets created and its parameters get initialized 
		self.app = Tk()
		self.app.title('TicTacToe')
		self.app.resizable(width=False, height=False)
# Object of Board class is created
		self.board = Board(first)
		
		self.font = Font(family="Helvetica", size=32)
		self.buttons = {}
		for x,y in self.board.fields:
			handler = lambda x=x,y=y: self.move(x,y,difficulty_level)
			button = Button(self.app, command=handler, font=self.font, width=2, height=1)
			button.grid(row=y, column=x)
			self.buttons[x,y] = button
		self.board= Board(first)
# If the first move needs to be made by the computer then the respective function is called and the gui is initialized with this move 
		if first == 0 and difficulty_level == 3:
			print("Wait a few seconds for the computer to make its move...")
			x,y,move,v = self.board.move2()
			self.board = self.board.move(self.board,y,x)
			self.board.temp_board[x][y] = 'X'

		if first == 0 and difficulty_level == 2:
			print("Wait a few seconds for the computer to make its move...")
			x,y,move,v = self.board.move2_medium()
			self.board = self.board.move(self.board,y,x)
			self.board.temp_board[x][y] = 'X'

		if first == 0 and difficulty_level == 1:
			x = random.choice([0,1,2,3])
			y = random.choice([0,1,2,3])
			self.board = self.board.move(self.board,y,x)
			self.board.temp_board[x][y] = 'X'
		self.update()
	
# This function is responsible for making the move each time 
# It makes two kinds of move one when the user clicks on a square and 
# one when a move needs to be made by our algorithm
	def move(self,x,y,difficulty_level):
# Make move is used to keep a track when the game gets over and no further move needs to be made
		global make_move  
		if make_move == 1:
# Move where the user selects a square 
			self.app.config(cursor="watch")
			self.app.update()

			self.board = self.board.move(self.board,x,y)
		
			self.update()
# Move where the computer plays for the corresponding difficulty levels 
			if difficulty_level == 3:
				x,y,move,v = self.board.move2()

				tup = (y,x)
				if move:
					self.board = self.board.move(self.board,y,x)
				else:
					self.board = self.board.move(self.board,y,x)
					for x,y in self.buttons:
						self.buttons[x,y]['state'] = 'disabled'

			if difficulty_level == 2:
				x,y,move,v = self.board.move2_medium()

				tup = (y,x)
				if move:
					self.board = self.board.move(self.board,y,x)
				else:
					self.board = self.board.move(self.board,y,x)
					for x,y in self.buttons:
						self.buttons[x,y]['state'] = 'disabled'	


			if difficulty_level == 1:
				x,y,move,v = self.board.move2_easy()

				tup = (y,x)
				if move:
					self.board = self.board.move(self.board,y,x)
				else:
					self.board = self.board.move(self.board,y,x)
					for x,y in self.buttons:
						self.buttons[x,y]['state'] = 'disabled'
			
			
			make_move = move
	

		self.update()
		self.app.config(cursor="")

# This fucntion updates the board each time a move is made by changing the button configurations 
	def update(self):
		for (x,y) in self.board.fields:
			text = self.board.fields[x,y]
			self.buttons[x,y]['text'] = text
			self.buttons[x,y]['disabledforeground'] = 'black'
			if text==self.board.empty:
				self.buttons[x,y]['state'] = 'normal'
			else:
				self.buttons[x,y]['state'] = 'disabled'

		for (x,y) in self.board.fields:
			self.buttons[x,y].update()

	def mainloop(self):
		self.app.mainloop()

if __name__ == '__main__':
	GUI().mainloop()
