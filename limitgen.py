import numpy as np
import random
from abjad import *

bank = [5.5,6.5,7,8,10,11.5,13,17.5,18.5,19,20,21.5,22.5,23,25,27]
min_distance = 1.5
max_distance = 7 # inclusive

container = [13]
for i in range(100):
	prev_note = container[i]
	newbank = []
	for pit in bank:
		if pit <= prev_note and pit >= prev_note-max_distance and pit <= prev_note-min_distance:
			newbank.append(pit)
		elif pit > prev_note and pit <= prev_note+max_distance and pit >= prev_note+min_distance:
			newbank.append(pit)
	print newbank
	container.append(random.choice(newbank))

cont = [Note(pit,1/8.) for pit in container]
staff = Staff(cont)
score = Score([staff])
show(score)