import numpy as np
import random
from collections import Counter
from abjad import *
from copy import deepcopy

# generate pitches
container = [5,6.5,11,15,12.5,6.5,8,13,10,15,13,18.5,18,13,18.5,20,17.5] # 1
container = [22,16.5,23,18.5,22,14,18.5,24.5,18.5,20,25,30,29,24.5,20,18.5] # 2

# make/show score
container = [Note(pit,1/8.) for pit in container]
instruments = set(['Flute'])
parts = {instrument: Staff([], name=instrument) for instrument in instruments}
parts['Flute'].extend(container)
score = Score([parts[instrument] for instrument in parts], name="poopy")
attach(MetronomeMark((1,4), 190), parts['Flute'][0])
show(score)

# # out to Sibelius?
# should_show = raw_input("Out to sibelius? (y/n)")
# if should_show == 'y':
# 	topleveltools.play(score)
