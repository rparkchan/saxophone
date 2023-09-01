### generate partial tone rows of length n <= 12, which, when played in sequence with the same tone row modulated or inverted by some transformation,
###     complete the original tone row with the first m = 12-n notes
### ex: a 9-note tone row [C, E, D, Ab, G, B, Bb, F#, A], followed by the same tone row up a half step [Db, F, Eb...] which completes the tone row
### also allows for finer grained control of how many notes you want to constrain to not overlap the original phrase (i.e. complete tone row): can be fewer than 12-n
### however m should always be >= 1, otherwise you can double the last note of the phrase as the first note of the modulation

import numpy as np
import random
from abjad import Note, Staff, Score, show, Rest

# random.seed(0)

ROW_LENGTH = 9
COMPLETION_LENGTH = 3 # should usually add up to 12 but can lower to be less strict if you notice the phrases suck lol. Basically makes it "less 12 tone"
MODULATION_AMOUNT = -1
RANGE_START = 11
MAXIMUM_INTERVAL = 7 # set to 12 for no constraint
DESIRED_NUMBER_PHRASES = 10

counter = 0
container = []
while (counter < DESIRED_NUMBER_PHRASES):
    newphrase = []
    bank = [*range(RANGE_START, RANGE_START + 12)]
    for j in range(COMPLETION_LENGTH):
        note = random.choice(bank)

        newphrase.append(note)
        bank.remove(note)
        if ((note + MODULATION_AMOUNT) % 12 + 12 in bank):
            bank.remove((note + MODULATION_AMOUNT) % 12 + 12)

    for k in range(ROW_LENGTH - COMPLETION_LENGTH):
        note = random.choice(bank)
        newphrase.append(note)
        bank.remove(note)
    
    differences = [j-i for i, j in zip(newphrase[:-1], newphrase[1:])]
    if any([abs(k) > MAXIMUM_INTERVAL for k in differences]):
        continue
    
    modulatedNewPhrase = [note + MODULATION_AMOUNT for note in newphrase]
    anotherModulatedNewPhrase = [note + MODULATION_AMOUNT * 2 for note in newphrase]
    container = container + newphrase + modulatedNewPhrase + anotherModulatedNewPhrase

    while (len(container) % 8 != 0):
        container.append('rest')
    
    counter += 1

cont = [Note(pitch,1/8.) if type(pitch) is int else Rest('r8') for pitch in container]
staff = Staff(cont)
score = Score([staff])
show(score)