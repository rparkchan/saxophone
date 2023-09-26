### generate arpeggio-like unidirectional line going from one chosen note to another using randomly chosen intervals

import numpy as np
import random
from abjad import Note, Staff, Score, show, Rest

# random.seed(0)

STARTING_PITCH = 3
ENDING_PITCH = 25
MAXIMUM_INTERVAL = 6 # set to 12 for no constraint
MINIMUM_INTERVAL = 1 # set to 1 for no constraint
INVERT = True

DESIRED_NUMBER_PHRASES = 25
POST_MODULATION = 0

counter = 0
container = []
while (counter < DESIRED_NUMBER_PHRASES):
    newphrase = []

    note = STARTING_PITCH
    while note <= ENDING_PITCH:
        newphrase.append(note)
        note += random.randint(MINIMUM_INTERVAL, MAXIMUM_INTERVAL)
        if (note >= ENDING_PITCH):
            newphrase.append(ENDING_PITCH)
            break
    
    if INVERT:
        newphrase.reverse()

    container += newphrase
    
    while (len(container) % 8 != 0):
        container.append('rest')
    
    counter += 1

cont = [Note(pitch + POST_MODULATION,1/8.) if type(pitch) is int else Rest('r8') for pitch in container]
staff = Staff(cont)
score = Score([staff])
show(score)