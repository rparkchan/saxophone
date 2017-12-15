import numpy as np
import random
from collections import Counter
from scales import getIntervals
from abjad import *
from copy import deepcopy

# constants
STARTING_NOTE = 15
NUM_PITCHES = 12
NUM_REPS = 32
POSSIBLE_RANGE = [2, 30]
STARTING_RANGE = [1,12]
RANGE_UPDATES = [1]
TEMPO = 190

# probabilities and updates
up_p = .5
P_UPDATES = {"up_p": .3}

# abjad initialization
instruments = set(['Flute'])
parts = {instrument: Staff([], name=instrument) for instrument in instruments}
current_note = STARTING_NOTE

# determine starting pitches
pitches = []
for i in range(NUM_PITCHES):
	while True:
		temp_pitch = random.randint(STARTING_RANGE[0], STARTING_RANGE[1])
		if temp_pitch not in pitches:
			pitches.append(temp_pitch)
			break

# generate notes
container = []
for i in range(NUM_REPS):
	for note in pitches:
		current_note = note
		container.append(Note(current_note, 1/8.))

	# if random.random() <= up_p:
	pitches = [pitch + random.choice(RANGE_UPDATES) for pitch in pitches]
	# up_p = up_p - P_UPDATES["up_p"]
	# else:
	# 	pitches = [pitch - random.choice(RANGE_UPDATES) for pitch in pitches]
	# 	up_p = up_p + P_UPDATES["up_p"]

	random.shuffle(pitches)

# make/show score
parts["Flute"].extend(container)
score = Score([parts[instrument] for instrument in parts], name="poopy")
attach(MetronomeMark((1,4), TEMPO), parts["Flute"][0])
show(score)

# out to Sibelius?
should_show = raw_input("Out to sibelius? (y/n)")
if should_show == "y":
	topleveltools.play(score)