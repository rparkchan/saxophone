### generate partial tone rows of length n <= 12, which, when played in sequence with the same tone row modulated or inverted by some transformation,
###     complete the original tone row with the first m = 12-n notes
### ex: a 9-note tone row [C, E, D, Ab, G, B, Bb, F#, A], followed by the same tone row up a half step [Db, F, Eb...] which completes the tone row

import numpy as np
import random
from abjad import Note, Staff, Score, show, Rest

random.seed(0)

ROW_LENGTH = 9
COMPLETION_LENGTH = 12 - ROW_LENGTH
MODULATION_AMOUNT = 2
RANGE_START = 12

container = []
for i in range(10):
    newphrase = []
    bank = [*range(RANGE_START, RANGE_START + 12)]
    # print(bank)
    for j in range(COMPLETION_LENGTH):
        note = random.choice(bank)
        while ((note + MODULATION_AMOUNT) % 12 + RANGE_START not in bank): # ensure you are picking a note whose modulation isn't already in the phrase
            note = random.choice(bank)

        newphrase.append(note)
        bank.remove(note)
        bank.remove((note + MODULATION_AMOUNT) % 12 + RANGE_START)

    for k in range(ROW_LENGTH - COMPLETION_LENGTH):
        note = random.choice(bank)
        newphrase.append(note)
        bank.remove(note)
    
    modulatedNewPhrase = [note + MODULATION_AMOUNT for note in newphrase]
    container = container + newphrase + modulatedNewPhrase

    while (len(container) % 8 != 0):
        container.append('rest')

cont = [Note(pitch,1/8.) if type(pitch) is int else Rest('r8') for pitch in container]
staff = Staff(cont)
score = Score([staff])
show(score)