### generate partial tone rows of length n <= 12, which, when played in sequence with the same tone row modulated or inverted by some transformation,
###     complete the original tone row with the first m = 12-n notes
### ex: a 9-note tone row [C, E, D, Ab, G, B, Bb, F#, A], followed by the same tone row up a half step [Db, F, Eb...] which completes the tone row
### also allows for finer grained control of how many notes you want to constrain to not overlap the original phrase (i.e. complete tone row): can be fewer than 12-n
### however m should always be >= 1, otherwise you can double the last note of the phrase as the first note of the modulation

import numpy as np
import random
from abjad import Note, Staff, Score, show, Rest, persist, Block, LilyPondFile, lilypond, io
import subprocess

# random.seed(0)

ROW_LENGTH = 9
COMPLETION_LENGTH = 3 # should usually add up to 12 but can lower to be less strict if you notice the phrases suck lol. Basically makes it "less 12 tone"
RANGE = 24
MODULATION_AMOUNT = 2
REPETITIONS = 7
MAXIMUM_INTERVAL = 12 # set to 1000 for no constraint
MINIMUM_INTERVAL = 1 # set to 1 for no constraint
DESIRED_NUMBER_PHRASES = 20
POST_MODULATION = 0

OPEN_LOGIC = True
SHOW_SCORE = True

counter = 0
container = []
while (counter < DESIRED_NUMBER_PHRASES):
    newphrase = []
    bank = [*range(0, RANGE)] # TODO: allow max range greater than 12, so have to remove all octaves of a note from the bank (in a loop over the bank I guess)
    completionbank = bank.copy()
    for _ in range(COMPLETION_LENGTH):
        note = random.choice(completionbank)
        newphrase.append(note)

        # remove all versions of the note and its modulation from the bank
        for banknote in bank[:]:
            if (banknote % 12 == note % 12 or banknote % 12 == (note + MODULATION_AMOUNT) % 12):
                bank.remove(banknote)

        # remove all versions of the note, its modulation, AND its inverse modulation from completion bank
        for completionbanknote in completionbank[:]:
            if (completionbanknote % 12 == note % 12 or completionbanknote % 12 == (note + MODULATION_AMOUNT) % 12 or completionbanknote % 12 == (note - MODULATION_AMOUNT) % 12 ):
                completionbank.remove(completionbanknote)

    for _ in range(ROW_LENGTH - COMPLETION_LENGTH):
        note = random.choice(bank)
        newphrase.append(note)

        for banknote in bank[:]:
            if (banknote % 12 == note % 12):
                bank.remove(banknote)
        
    combinedphrases = []
    for i in range(REPETITIONS):
        combinedphrases += [note + MODULATION_AMOUNT * i for note in newphrase]

    differences = [j-i for i, j in zip(combinedphrases[:-1], combinedphrases[1:])]
    if any([abs(k) > MAXIMUM_INTERVAL or abs(k) < MINIMUM_INTERVAL for k in differences]):
        continue

    container += combinedphrases

    container.append('rest')

    while (len(container) % 8 != 0):
        container.append('rest')
    
    counter += 1

cont = [Note(pitch + POST_MODULATION,1/8.) if type(pitch) is int else Rest('r8') for pitch in container]
staff = Staff(cont)
score = Score([staff])

# in order to generate midi. We create a lilypond file string, manipulate it because
# abjad defaults are horrendous, insert a `\midi { }` block, and then run lilypond on it
file = LilyPondFile([score])
lilypondString = lilypond(file).replace('<<', '{').replace('>>', '}').replace('new Score', 'score')
index = lilypondString.find('}')
withMidiBlock = lilypondString[:index + 1] + '\n    \midi { }' + lilypondString[index + 1:]
with open('output/lines.ly', 'w') as textfile:
    textfile.write(withMidiBlock)

if (OPEN_LOGIC):
    io.run_lilypond('./output/lines.ly')
    FileName = "./output/lines.midi"
    subprocess.call(['open', FileName])
if (SHOW_SCORE):
    show(score)