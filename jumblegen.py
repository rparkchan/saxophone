import numpy as np
import random
from abjad import *

scales = [[25,21.5,19,17.5],[25,22.5,20.5,19],[25,21.5,20,18.5]]
scales = [[22.5,20,18,17.5],[20,18.5,17.5,13],[10.5,13,8.5,7]]

container = []
for i in range(30):
	scale = scales[i % len(scales)]
	random.shuffle(scale)
	if i > 0 and scale[0] == container[len(container) - 1]:
		del(container[len(container) - 1])
	container = container + scale

cont = [Note(pit,1/8.) for pit in container]
staff = Staff(cont)
score = Score([staff])
show(score)