import numpy as np
import random
from collections import Counter
from abjad import *
from copy import deepcopy

# constants
INTERVAL_JUMP = 1
NUM_REPS = 40
TEMPO = 240

# varyings
up_p = .8
curr_bank = range(6,11)

# abjad initialization
instruments = set(['Flute'])
parts = {instrument: Staff([], name=instrument) for instrument in instruments}

# generate pitches
number_container = []
for i in range(NUM_REPS):
	for j in range(len(curr_bank)):
		prev_note = number_container[len(number_container) - 1] if number_container else 0
		curr_note = random.choice(curr_bank)
		if curr_note == prev_note:
			curr_note = curr_note + random.choice([1,-1])
		number_container.append(curr_note)

	if random.random() < up_p:
		curr_bank = [pitch + INTERVAL_JUMP for pitch in curr_bank]
	else:
		curr_bank = [pitch - INTERVAL_JUMP for pitch in curr_bank]

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