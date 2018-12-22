# pywav
A sound processing library based on numpy, and a software synthesizer.

PyWave library is designed to have these main features:
- Manipulate audios
- Easy to use 
- Make heavy use of numpy, so that it is powerful  and understandable 
- Compose music(loop) from samples
Will make use of existing music note text  format, e.g. MIDI, lilypond, mma


Example of usage 

Load wav file: 
a=Wave('a.wav')

Save to wav file:
a.save('a.wav')

Mix 2 audios from start:
c = a | b

Concatenate 2 audios, head to tail:
c = a + b
a += b

Amplify an audio by 2: 
c = a * 2

Mix an audio from specified place: 
a[1.5:]+=b

Resample at a different  rate 
a %= 44100

Trunc to a certain length:
a[:2.0]

Or 
Wave._Tempo = 120   # That's 0.5 second per beat
a/4   # 1 beat 
a/8   # half beat 
a/2   # 2 beats, 1 second
a/2.5 # 3 beats, 1.5 seconds
a/4.5 # 1.5 beat, 0.75 seconds

If the audio is shorter than the length, silence will be added. 

It is implemented as files. Later on when it is more stable and has more 
   subscribers, it will be turned into a package. 
   
