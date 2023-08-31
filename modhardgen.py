### given a phrase, repeat it n times modulated m amount

import numpy as np
import random
from abjad import Note, Staff, Score, show, Rest

# random.seed(0)

PHRASE = [24, 22, 14, 19, 21, 18, 16, 20, 17]
MODULATION_AMOUNT = -1

container = PHRASE.copy()
for i in range(12):
    modulatedNewPhrase = [note + MODULATION_AMOUNT * (i + 1) for note in PHRASE]
    container = container + modulatedNewPhrase

cont = [Note(pitch,1/8.) if type(pitch) is int else Rest('r8') for pitch in container]
staff = Staff(cont)
score = Score([staff])
show(score)