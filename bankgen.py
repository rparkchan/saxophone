import numpy as np
import random
import math
from collections import Counter
from abjad import *
from copy import deepcopy

# # HIGH
# BANK = [27,26.5,26,25.5,25,24.5,24,23.5,23,22.5,22,21.5,21,20.5,20,19,18.5,18,17.5,17,16.5,16]

# # ALL
# BANK = [5,5.5,6,6.5,7,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,14,14.5,15,15.5,16,16.5,17,17.5,18,18.5,19,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27]

# SCALE 0
BANK = [3,5,6.5,8,9.5,10.5,11,13,15,17,18.5,20,21.5,22.5,23,25,27]

# intervals
MAIN_INTERVALS = [3,5]
EXTRA_INTERVALS = [1,2,3,4,5,6,6,7,7,8,8,9,10,11,12]

# constants
NUM_REPEATED_PHRASES = 5
REPEATED_PHRASE_LENGTHS = [3,5,7,9]
NUM_NOTES = 8
P_IN = {"up_p": .5, "half_p": .5, "intervalic_p": .3, "rest_p": .000, "rep_p": 0}
P_UP = {"up_p": .2, "half_p": .5, "intervalic_p": .15, "rest_p": .000, "rep_p": 0}

# varyings
up_p = P_IN["up_p"]
half_p = P_IN["half_p"]
intervalic_p = P_IN["intervalic_p"]
rest_p = P_IN["rest_p"]
rep_p = P_IN["rep_p"]
counter = 0
go_up = True

# fill container with pitches
container = []
for i in range(10):
	START_WITH = False
	curr_index = BANK.index(17.)
	direction = 1
	step_size = 0
	for j in range(NUM_NOTES):
		# add newest note 
		container.append(BANK[curr_index])

		# update probabilities and varyings: keep within range
		up_p = up_p - P_UP["up_p"] if direction == 1 else up_p + P_UP["up_p"]
		if (step_size == MAIN_INTERVALS[0]):
			half_p = half_p - P_UP["half_p"]
		elif (step_size == MAIN_INTERVALS[1]):
			half_p = half_p + P_UP["half_p"]
		intervalic_p = intervalic_p + P_UP["intervalic_p"]
		rest_p = rest_p + P_UP["rest_p"]

		# main step
		step_size = MAIN_INTERVALS[0] if random.random() < half_p else MAIN_INTERVALS[1]

		# extra step
		if (random.random() < intervalic_p):
			step_size = random.choice(EXTRA_INTERVALS)
			intervalic_p = P_IN["intervalic_p"]

		# direction
		if (curr_index - step_size < 0):
			up_p = 1
		elif (curr_index + step_size >= len(BANK)):
			up_p = 0
		direction = 1 if random.random() < up_p else -1	

		# update index
		curr_index = curr_index + step_size * direction

	# add rests
	for k in range(8): container.append(11)


# make/show score
cont = [Note(pit,1/8.) for pit in container]
if not START_WITH:
	cont.reverse()
staff = Staff(cont)
score = Score([staff])
show(score)

# out to Sibelius?
# should_show = raw_input("Out to sibelius? (y/n)")
# if should_show == 'y':
# 	topleveltools.play(score)
