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
SCALE = [0,2,4,7,9]
MAIN_INTERVALS, EXTRA_INTERVALS = getIntervals(SCALE)
# print MAIN_INTERVALS, EXTRA_INTERVALS
MAIN_INTERVALS = [1,1]
EXTRA_INTERVALS = [4,3]

# constants
RANGE = {"bottom": 6, "top": 15}
RANGE_UPDATE = 1
NUM_NOTES_RANGE_UPDATE = 10
NUM_REPEATED_PHRASES = 5
REPEATED_PHRASE_LENGTHS = [3,5,7,9]
STARTING_NOTE = 12
NUM_NOTES = 8 * 48
TEMPO = 190
P_BASELINE = {"up_p": .5, "half_p": .5, "intervalic_p": .1, "rest_p": .000, "rep_p": 0}
P_UPDATES = {"up_p": .1, "half_p": .4, "intervalic_p": .00, "rest_p": .000, "rep_p": 0}

# varyings
up_p = P_BASELINE["up_p"]
half_p = P_BASELINE["half_p"]
intervalic_p = P_BASELINE["intervalic_p"]
rest_p = P_BASELINE["rest_p"]
rep_p = P_BASELINE["rep_p"]
counter = 0
go_up = True

# initials
direction = 1 if random.random() < up_p else -1
step_size = MAIN_INTERVALS[0] if random.random() < half_p else MAIN_INTERVALS[1]

# abjad initialization
instruments = set(['Flute'])
parts = {instrument: Staff([], name=instrument) for instrument in instruments}
current_note = STARTING_NOTE

# generate initial set of notes
container = []
for i in range(NUM_NOTES):
	current_note = current_note + step_size * direction
	container.append(Note(current_note, 1/8.))

	# update probabilities and varyings: keep within range
	up_p = up_p - P_UPDATES["up_p"] if direction == 1 else up_p + P_UPDATES["up_p"]
	if (step_size == MAIN_INTERVALS[0]):
		half_p = half_p - P_UPDATES["half_p"]
	elif (step_size == MAIN_INTERVALS[1]):
		half_p = half_p + P_UPDATES["half_p"]
	intervalic_p = intervalic_p + P_UPDATES["intervalic_p"]
	rest_p = rest_p + P_UPDATES["rest_p"]

	# direction
	if (current_note <= RANGE["bottom"]):
		up_p = 1
	elif (current_note >= RANGE["top"]):
		up_p = 0
	direction = 1 if random.random() < up_p else -1	

	# main step
	step_size = MAIN_INTERVALS[0] if random.random() < half_p else MAIN_INTERVALS[1]

	# extra step
	if (random.random() < intervalic_p):
		step_size = random.choice(EXTRA_INTERVALS)
		intervalic_p = P_BASELINE["intervalic_p"]

	# rest
	if (random.random() < rest_p):
		container.append(Rest('r8'))
		rest_p = P_BASELINE["rest_p"]

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
		if counter == 0:
			go_up = True
		if counter > 10:
			go_up = False

# repeat phrases (constant probability)
repeated_container = deepcopy(container)
for j in range(len(container) - 2*(max(REPEATED_PHRASE_LENGTHS)-1) - 1):
	if random.random() <= rep_p:
		phrase_length = random.choice(REPEATED_PHRASE_LENGTHS)
		for k in range(phrase_length):
			repeated_container[j + k + phrase_length] = container[j + k]

# make/show score
parts['Flute'].extend(repeated_container)
score = Score([parts[instrument] for instrument in parts], name="poopy")
attach(MetronomeMark((1,4), TEMPO), parts['Flute'][0])
show(score)

# out to Sibelius?
should_show = raw_input("Out to sibelius? (y/n)")
if should_show == 'y':
	topleveltools.play(score)
