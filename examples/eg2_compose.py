from pywav import Wave, rest 

prefix='eg1_ukulele_'

def n(note): 
    return Wave(prefix + note  + '.wav') 

def test_composing(): 
    c4=n('C4')
    d4=n('D4')  
    e4=n('E4') 
    f4=n('F4') 
    g4=n('G4') 
    c5=n('C5') 
    
    l=0.5
    l2=l*2 
    l4=l*4 
    Wave._tempo = 120 
    
    # Here's the song "Roll Roll Roll Your Boat" 
    a =  [ 
        c4/2, 
        c4/2, 
        c4/4, d4/4 ,
        e4/4, 
        rest/4,
         
        e4/4, d4/4, 
        e4/4, f4/4, 
        g4/1, 
        
        c5/4, c5/4, 
        g4/4, g4/4, 
        e4/4, e4/4, 
        c4/4, c4/4, 
        
        g4/4, f4/4, 
        e4/4, d4/4, 
        c4/1
        ] 
    a2=None
    for item in a : 
        if a2 is not None: 
            a2 += item 
        else: 
            a2 = item 
        print(item.length()) 
    
    # save to file
    f='eg2_roll.wav' 
    a2.save(f) 
    print(f, 'is created.') 
    
    # play the music 
    # print( 'Play finish.') 
    # a2.play() 

    

if __name__ == '__main__': 
    test_composing() 



