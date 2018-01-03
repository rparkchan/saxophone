import numpy as np
import random
from collections import Counter
from abjad import *
from copy import deepcopy

def swap_two(swap_list):
	choices = range(0, len(swap_list))
	ind_1 = random.choice(choices)
	ind_2 = random.choice([choice for choice in choices if choice != ind_1])
	swap_list[ind_1], swap_list[ind_2] = swap_list[ind_2], swap_list[ind_1]

	return swap_list

# constants
NUM_REPS = 13
TEMPO = 240
TRANSPOSE = 13

# varyings 
curr_range = range(18,23)
up_p = .5
phrase = [0,1,6,7,3,8,9,5,11]
phrase = [pitch + TRANSPOSE for pitch in phrase]

# abjad initialization
instruments = set(['Flute'])
parts = {instrument: Staff([], name=instrument) for instrument in instruments}

# generate pitches
number_container = []
for i in range(NUM_REPS):
	last_entry = number_container[len(number_container) - 1] if len(number_container) >= 2 else 0
	if last_entry == phrase[0]:
		phrase = [pitch + 1 for pitch in phrase]

	number_container  = number_container + phrase
	phrase = swap_two(phrase)
	if random.random() < up_p:
		phrase = [pitch + 1 for pitch in phrase]

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