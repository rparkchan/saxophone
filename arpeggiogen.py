### generate arpeggio-like line going from one chosen note to another

import numpy as np
import random
from abjad import Note, Staff, Score, show, Rest

# random.seed(0)

STARTING_PITCH = 0
ENDING_PITCH = 23
MAXIMUM_INTERVAL = 8 # set to 12 for no constraint
MINIMUM_INTERVAL = 1 # set to 1 for no constraint

DESIRED_NUMBER_PHRASES = 10
POST_MODULATION = 0

counter = 0
container = []
while (counter < DESIRED_NUMBER_PHRASES):
    newphrase = []

    note = STARTING_PITCH
    while note <= ENDING_PITCH:
        container.append(note)
        note += random.randint(MINIMUM_INTERVAL, MAXIMUM_INTERVAL)
        if (note >= ENDING_PITCH):
            container.append(ENDING_PITCH)
            break
    
    while (len(container) % 8 != 0):
        container.append('rest')
    
    counter += 1

cont = [Note(pitch + POST_MODULATION,1/8.) if type(pitch) is int else Rest('r8') for pitch in container]
staff = Staff(cont)
score = Score([staff])
show(score)