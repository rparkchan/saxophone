import numpy as np
import random
from collections import Counter
from abjad import *
from copy import deepcopy

container = []
intervals = [.5, 1.5, 2.5, 3.5]
for interval in intervals:
	starting_pitch = 25
	while (starting_pitch > 16):
		if (starting_pitch != 19.5 and starting_pitch - interval != 19.5 and starting_pitch - 2*interval != 19.5):
			container.append(starting_pitch)
			container.append(starting_pitch - interval)
			container.append(starting_pitch - 2*interval)
		else:
			container.append(11)
			container.append(11)
			container.append(11)
		for i in range(5):
			container.append(11)
		starting_pitch -= 1/2.
	for j in range(8):
		container.append(30)

# make/show score
container = [Note(pit,1/8.) for pit in container]
instruments = set(['Flute'])
parts = {instrument: Staff([], name=instrument) for instrument in instruments}
parts['Flute'].extend(container)
score = Score([parts[instrument] for instrument in parts], name="poopy")
attach(MetronomeMark((1,4), 160), parts['Flute'][0])
show(score)