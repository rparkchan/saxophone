import numpy as np
import random
from collections import Counter
from abjad import *
from copy import deepcopy

container = []
pitches = set([18, 18.5, 19, 20, 24])
last_pitch = 16
for i in range(100):
	curr_pitch = random.choice(list(pitches - set([last_pitch])))
	container.append(curr_pitch)
	last_pitch = curr_pitch

# make/show score
container = [Note(pit,1/8.) for pit in container]
instruments = set(['Flute'])
parts = {instrument: Staff([], name=instrument) for instrument in instruments}
parts['Flute'].extend(container)
score = Score([parts[instrument] for instrument in parts], name="poopy")
attach(MetronomeMark((1,4), 160), parts['Flute'][0])
show(score)