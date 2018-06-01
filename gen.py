import numpy as np
import random
from collections import Counter
from abjad import *
from copy import deepcopy

# return a list of the two most common intervals and then all other possible intervals
def getIntervals(scale):
	all_intervals = []
	for i in range(len(scale)):
		for j in range(len(scale)):
			if (i != j):
				all_intervals.append(abs(scale[i] - scale[j]))
	cntr = Counter(all_intervals)

	main_intervals = [cntr.most_common(2)[0][0], cntr.most_common(2)[1][0]]
	alt_intervals = [interval for interval in all_intervals if interval not in main_intervals]

	return main_intervals, alt_intervals

# intervals
# SCALE = [0,2,4,7,9]
# MAIN_INTERVALS, EXTRA_INTERVALS = getIntervals(SCALE)
MAIN_INTERVALS = [4,5]
EXTRA_INTERVALS = [1,1,1,2,2,2,3,5,6,6,7,7,8,9]
# MAIN_INTERVALS = [4,5]
# EXTRA_INTERVALS = [1,2,3,5,6,6,7,7,8,8,9]

# constants
RANGE = {"bottom": 6, "top": 15}
RANGE_UPDATE = 1
NUM_NOTES_RANGE_UPDATE = 10
NUM_REPEATED_PHRASES = 5
REPEATED_PHRASE_LENGTHS = [3,5,7,9]
STARTING_NOTE = 12
NUM_NOTES = 8 * 48
TEMPO = 190
P_IN = {"up_p": .5, "half_p": .5, "intervalic_p": .3, "rest_p": .000, "rep_p": 0}
P_UP = {"up_p": .4, "half_p": .4, "intervalic_p": .15, "rest_p": .000, "rep_p": 0}

# varyings
up_p = P_IN["up_p"]
half_p = P_IN["half_p"]
intervalic_p = P_IN["intervalic_p"]
rest_p = P_IN["rest_p"]
rep_p = P_IN["rep_p"]
counter = 0
go_up = True

# initials
direction = 1 if random.random() < up_p else -1
step_size = MAIN_INTERVALS[0] if random.random() < half_p else MAIN_INTERVALS[1]
current_pitch = STARTING_NOTE

# generate initial set of notes
container = []
for i in range(NUM_NOTES):
	current_pitch = current_pitch + step_size * direction
	container.append(current_pitch)

	# update probabilities and varyings: keep within range
	up_p = up_p - P_UP["up_p"] if direction == 1 else up_p + P_UP["up_p"]
	if (step_size == MAIN_INTERVALS[0]):
		half_p = half_p - P_UP["half_p"]
	elif (step_size == MAIN_INTERVALS[1]):
		half_p = half_p + P_UP["half_p"]
	intervalic_p = intervalic_p + P_UP["intervalic_p"]
	rest_p = rest_p + P_UP["rest_p"]

	# direction
	if (current_pitch <= RANGE["bottom"]):
		up_p = 1
	elif (current_pitch >= RANGE["top"]):
		up_p = 0
	direction = 1 if random.random() < up_p else -1	

	# main step
	step_size = MAIN_INTERVALS[0] if random.random() < half_p else MAIN_INTERVALS[1]

	# extra step
	if (random.random() < intervalic_p):
		step_size = random.choice(EXTRA_INTERVALS)
		intervalic_p = P_IN["intervalic_p"]

	# rest
	if (random.random() < rest_p):
		container.append(Rest('r8'))
		rest_p = P_IN["rest_p"]

	# range
	if i % NUM_NOTES_RANGE_UPDATE == 0:
		if go_up:
			RANGE["bottom"] = RANGE["bottom"] + RANGE_UPDATE
			RANGE["top"] = RANGE["top"] + RANGE_UPDATE
			counter = counter + 1
		else:
			RANGE["bottom"] = RANGE["bottom"] - RANGE_UPDATE
			RANGE["top"] = RANGE["top"] - RANGE_UPDATE	
			counter = counter - 1
		# if random.random() <= .5:
		# 	go_up = True
		# else:
		# 	go_up = False
		if counter % 10 == 0:
			go_up = True
		elif counter % 10 == 5:
			go_up = False

# make/show score
container = [Note(pit,1/8.) for pit in container]
instruments = set(['Flute'])
parts = {instrument: Staff([], name=instrument) for instrument in instruments}
parts['Flute'].extend(container)
score = Score([parts[instrument] for instrument in parts], name="poopy")
attach(MetronomeMark((1,4), TEMPO), parts['Flute'][0])
show(score)

# # out to Sibelius?
# should_show = raw_input("Out to sibelius? (y/n)")
# if should_show == 'y':
# 	topleveltools.play(score)
