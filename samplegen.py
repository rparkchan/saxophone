### given two short melodies (in any key), combine them with some modifications (inversion, modulation, permutation, insertion, etc.) in random ways to try and make nice lines
### inspired by (C# F# G# A#) (G A F D C# Eb Ab Bb C), where the A# G A F is effectively a sample from the Mew theme from Pokemon Movie the First

import numpy as np
import random
from abjad import Note, Staff, Score, show, Rest

melodyOne = [13, 16, 20, 18, 13] # from Tatami Galaxy OST 19: https://www.youtube.com/watch?v=90uIcEfXgrQ
melodyTwo = [16, 18, 20, 18, 23, 20] # from Bubble Gum by Clairo: https://soundcloud.com/user-541140906/clairo-bubblegum-live
# melodyTwo = [21, 25, 23, 18, 17] # from Tatami Galaxy OST 19: https://www.youtube.com/watch?v=90uIcEfXgrQ

P_INVERT = 0.0
MODULATION_RANGE = range(-5, 5)
P_INSERT = 0.1

container = []
for i in range(5):
	modifiedMelodyOne = melodyOne[::-1] if random.random() < P_INVERT else melodyOne[:]
	modifiedMelodyTwo = melodyTwo[::-1] if random.random() < P_INVERT else melodyTwo[:]
	# test to make sure I'm not messing up the originals

	modulationOne = random.choice(MODULATION_RANGE)
	modulationTwo = random.choice(MODULATION_RANGE)

	modifiedMelodyOne = [pitch + modulationOne for pitch in modifiedMelodyOne]
	modifiedMelodyTwo = [pitch + modulationTwo for pitch in modifiedMelodyTwo]

	container = container + modifiedMelodyOne + modifiedMelodyTwo

	while (len(container) % 8 != 0):
		container.append('rest')

cont = [Note(pitch,1/8.) if type(pitch) is int else Rest('r8') for pitch in container]
staff = Staff(cont)
score = Score([staff])
show(score)