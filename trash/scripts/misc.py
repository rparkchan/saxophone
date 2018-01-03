import numpy as np
import random
from collections import Counter
from scales import getIntervals
from abjad import *
from copy import deepcopy

# constants
STARTING_NOTE = 15
NUM_REPS = 20
POSSIBLE_RANGE = [2, 30]
STARTING_RANGE = [15,26]
TEMPO = 240
PATTERN_LENGTHS = [random.randint(5,11) for i in range(50)]

# abjad initialization
instruments = set(['Flute'])
parts = {instrument: Staff([], name=instrument) for instrument in instruments}
current_note = STARTING_NOTE

# generate patterns
patterns = []
for length in PATTERN_LENGTHS:
	pattern = []
	for i in range(length):
		while True:
			temp_pitch = random.randint(STARTING_RANGE[0], STARTING_RANGE[1])
			if temp_pitch not in pattern:
				pattern.append(temp_pitch)
				break
	patterns.append(pattern)

# generate pitches, increment when we run into repetitions
number_container = []
for i in range(NUM_REPS):
	pattern = random.choice(patterns)
	last_pitch = number_container[len(number_container)-1] if number_container else 0

	# increment with repetition
	if last_pitch == pattern[0]:
		pattern = [pitch + 1 for pitch in pattern]
		for j in range(len(patterns)):
			patterns[j] = [pitch + 1 for pitch in patterns[j]]
		
	for pitch in pattern:
		number_container.append(pitch)

# generate notes
container = []
for number in number_container:
	container.append(Note(number, 1/8.))

# make/show score
parts["Flute"].extend(container)
score = Score([parts[instrument] for instrument in parts], name="poopy")
attach(MetronomeMark((1,4), TEMPO), parts["Flute"][0])
show(score)

# # out to Sibelius?
should_show = raw_input("Out to sibelius? (y/n)")
if should_show == "y":
	topleveltools.play(score)