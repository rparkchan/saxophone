import numpy as np
import random
from collections import Counter
from scales import getIntervals
from abjad import *
from copy import deepcopy

# constants
STARTING_NOTE = 15
NUM_NOTES = 32
POSSIBLE_RANGE = [2, 30]
TEMPO = 170

# abjad initialization
instruments = set(['Flute'])
parts = {instrument: Staff([], name=instrument) for instrument in instruments}
current_note = STARTING_NOTE

# determine starting pitches

# generate notes
container = []
for i in range(NUM_NOTES):
	current_note = note
	container.append(Note(current_note, 1/8.))

# make/show score
parts["Flute"].extend(container)
score = Score([parts[instrument] for instrument in parts], name="poopy")
attach(MetronomeMark((1,4), TEMPO), parts["Flute"][0])
# show(score)

# out to Sibelius?
# should_show = raw_input("Out to sibelius? (y/n)")
# if should_show == "y":
topleveltools.play(score)