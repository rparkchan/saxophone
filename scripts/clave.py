import numpy as np
import random
from collections import Counter
from abjad import *
from copy import deepcopy

# constants
NUM_REPS = 13
TEMPO = 240
CLAVES = [[1,0,0,1,0,0,1,0,0,0,1,0,0,0,1,0], [0,0,1,0,1,0,0,0,1,0,0,1,0,0,1,0]]

# varyings 
curr_range = range(18,23)
up_p = .5

# abjad initialization
instruments = set(['Flute'])
parts = {instrument: Staff([], name=instrument) for instrument in instruments}

# generate pitches
number_container = []
for k in range(NUM_REPS):
	for i in range(len(CLAVES)):
		clave = CLAVES[i]
		moving_pitch = random.choice(curr_range)
		for j in range(len(clave)):
			if clave[j]:
				curr_note = moving_pitch
			else:
				prev_note = number_container[len(number_container) - 1] if number_container else 0
				curr_note = random.choice([pitch for pitch in curr_range if pitch != prev_note and pitch != moving_pitch])
			number_container.append(curr_note)
		# curr_range = [pitch + 1 for pitch in curr_range]

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