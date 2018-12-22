from pywav import Wave
import numpy as np 

a = Wave ('eg1_ukulele_samples_noice_reduced.wav') 
prefix='eg1_ukulele_'
 
notes = [
    #name, start, end  (in seconds) 
    ('C4', 5.455, 9.526), 
    ('D4', 12.066, 15.806), 
    ('E4', 16.882, 18.964), 
    ('F4', 22.937, 25.067), 
    ('G4', 29.278, 31.241), 
    ('A5', 34.950, 37.098), 
    ('B5', 41.120, 42.725), 
    ('C5', 46.209, 47.788), 
    ] 

# loop and split each note
for n, start, end in notes: 
    a[start:end].save( prefix+n+'.wav') 
    print(n) 
    

