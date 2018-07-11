import numpy as np
import random
from collections import Counter
from abjad import *
from copy import deepcopy

# generate pitches
containers = []
containers.append([18.5,19,17.5,13,12.5,18.5,19,17.5,13,12]) 
containers.append([5,6.5,11,5.5,12.5,8,7,11.5,12.5,15,13,18.5,19])
containers.append([22,16.5,23,18.5,22,14,18,24.5,18.5,23,25,30,29,24.5,20,18.5])
containers.append([24.5,26,20.5,19,'r',24,23,21.5,18.5,20,17.5,13,12.5,17.5,22.5,20,20.5,19,16.5,13,20,21.5,21])
containers.append([0,7,13,18,12,'r',13,15,11,0,7])
containers.append([22.5,17.5,13,21,18.5,23,17.5,13,19,18.5]) 
containers.append([23.5,25,20,18.5,18,23.5,25,20,18.5,17])
containers.append([23,25,21.5,19,17.5,23.5,25,20,18.5,19,17.5,13,12.5,18.5,20,17.5,19])
containers.append([9.5,11,6.5,11,12,9.5,13.5,10,6.5,8.5,13,5.5,7,9.5,8,12,10.5,13,11,14.5])
containers.append([21.5,23,25,27,22.5,20])
containers.append([23,21.5,25,27,21.5,20,25,21.5])
containers.append([23,20.5,19,17.5,21,18.5,21.5,17,18.5,21.5,17.5,20,18.5,19,21.5,23,18.5,22])
containers.append([20,21.5,17.5,19])

# make staves from containers, with markups
count = 0
staff = []
for i, container in enumerate(containers):
	cont = [Note(pit,1/8.) if isinstance(pit,float) or isinstance(pit,int) else Rest('r8') 
								for pit in container]
	for note in cont:
		staff.append(note)
		count += 1
	while (count % 8 != 0):
		staff.append(Rest('r8'))
		count += 1
	staff.append(Rest('r1'))

# show score
score = Score([Staff(staff)])
show(score)