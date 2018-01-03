import numpy as np
import random
from collections import Counter
from abjad import *
from copy import deepcopy

# constants
TEMPO = 240
NUM_REPS = 13
B_INT = [8,9,10]
PHRASE_LENGTHS = [6,7]

# varyings 
curr_range = range(10,18)
up_p = .5

# abjad initialization
instruments = set(['Flute'])
parts = {instrument: Staff([], name=instrument) for instrument in instruments}

# generate pitches
number_container = []
for i in range(NUM_REPS):
	temp_range = deepcopy(curr_range)
	phrase_len = random.choice(PHRASE_LENGTHS)

	for j in range(phrase_len):
		pick = random.choice(temp_range)
		temp_range.remove(pick)
		number_container.append(pick)

	update = 1 if i < 4 else -1
	curr_range = [pitch + update for pitch in curr_range]

	number_container.append(number_container[len(number_container) - 1] + random.choice(B_INT))

# generate notes
container = []
for number in number_container:
	container.append(Note(number, 1/8.))

# make/show score
parts["Flute"].extend(container)
score = Score([parts[instrument] for instrument in parts], name="poopy")
attach(MetronomeMark((1,4), TEMPO), parts["Flute"][0])
show(score)

# out to Sibelius?
should_show = raw_input("Out to sibelius? (y/n)")
if should_show == "y":
	topleveltools.play(score)