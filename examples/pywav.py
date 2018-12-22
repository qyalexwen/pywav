# For reading wave file and calculation
import scipy.io.wavfile as wf 
import numpy as np 

# for playback 
import sounddevice
import time
import keyboard as kb 

CD_RATE = 44100 

class Wave(object): 
    _tempo = 120 # static variable 
    rate = CD_RATE 
    samples = None
    
    def __init__(self, filename=None): 
        if filename: 
            rate, wave = wf.read(filename) 
            self.rate = rate 
            self.samples = wave 
            self.normalize() 
    
    def set_samples(self, samples): 
        self.samples = samples 
        
    def copy(self): 
        r = Wave() 
        samples = self.samples.copy() 
        r.set(samples, self.rate) 
        return r
    
    def __eq__(self, other): 
        return (self.rate == other.rate) and \
            ( np.array_equal(self.samples, other.samples) ) 
        
    def set(self, samples, rate=CD_RATE): 
        # print('samples=', samples) 
        self.samples = samples 
        self.rate = rate
        
    def print(self): 
        print('Rate is', self.rate)
        print('Samples', self.samples[:5] ) 
        print('Range', min(self.samples), max(self.samples) )
        
        print('Type', self.samples.dtype) 
        
    def __len__(self): 
        return len(self.samples) / self.rate 
    
    def length(self): 
        return self.__len__() 
    
    def normalize(self): 
        min0= abs( min(self.samples))
        max0= abs(max(self.samples))
        m = float(max( min0,max0  )  ) 
        # print(m) 
        s2 = self.samples.copy().astype(np.float32) 
        if m>0 : 
            s2 /= m 
        self.samples = s2 
            
    def mix(self, other, start, end=None, cut=True, ratio=1): 
        ''' Mix 2 audio together, at a certain position
        other -- the other audio to mix with
        start -- position at the current audio to be mixed 
        end   -- end position. If None, then mix to the maximum length
        cut   -- If the other audio is longer than the current one, 
                     it will be cut if "cut" is True 
        radio -- When mix, multiply the other audio with this ratio, 
                  default is 1 
        '''
        rate=self.rate 
        rate2=other.rate 
        w2=other.samples
        
        if rate != rate2: 
            # to do: raise an exception 
            print('Rate not match', rate2) 
            return None 
            
        # calculate proper length for both audios
        # There are several cases: 
        # 1. Cut = True, len1 >= len2, mix according to len2 
        # 2. Cut = True, len1 < len2,  mix according to len1 
        # 3. Cut = False, len1 >=len2, mix according to len2 
        # 4. Cut = False, len1 < len2, extend len1, and mix according to len2 
        #  So, 1 and 3 are the same. 

        start0 = int(rate * start) 
        len1 = len(self.samples)-start0 if end is None else int(rate*end) 
        len2 = len(w2) 
        
        len3 = 0
        out = self.samples.copy()  
        if len1 >= len2: # branch 1 and 3 
            len3 = len2 
        elif cut:  # branch 2 
            len3 = len1 
        else:   # branch 4 
            # extend 
            out = np.zeros(start0 + len2)
            out[:len(self.samples)] = self.samples  
            len3 = len2
             
        out[start0:start0+len3] += w2[:len3]*ratio
        
        self.set_samples(out) 
        
    def mul(self, rate): 
        self.samples = self.samples * rate 
    
    def imul(self, other): 
        self.mul(other) 
 
    def __truediv__(self, other): 
        n = int( self.rate * 60 *4 / ( self._tempo * other)) 
        a = Wave()
        a.set_samples(self.samples[:n]  ) 
        return a 
        
    def save(self, filename, output=False): 
        self.normalize() 
        wf.write( filename, self.rate, self.samples) 
        if output: 
            print(filename, 'is created.') 

    def __add__(self, w2): 
        if self.rate != w2.rate: 
            print("Rates don't match", self.rate, w2.rate) 
            return None 
        else: 
            samples = np.concatenate([ self.samples, w2.samples] ) 
            c = Wave()
            c.set_samples(samples) 
            return c
    
    def piece(self, start, end): 
        rate=self.rate 
        start0 = int(rate * start) 
        end0 = int(rate * end) 
        oc=Wave() 
        oc.set(self.samples[start0:end0], rate) 
        return oc

    def play(self): 
        x  = (self.samples*32768).astype(np.int16)  # scale to int16 for sound card
        sounddevice.play(x)
        
        # wait for keypress 
        print('Press q to quit.') 
        while True: 
            if kb.is_pressed('q') : 
                break 
            time.sleep(1) 
            
    def __getitem__(self, key): 
        # example  w[ start_second : end_second ]
        if type(key) is slice: 
            
            start_sample = int( self.rate * (key.start if key.start else 0 ) ) 
            stop_sample = int ( self.rate * key.stop ) 
            # calculate length. If length is longer than samples, fill with 0 
            samples = self.samples[ start_sample: stop_sample] 
            w = Wave()
            w.set( samples, self.rate)
            return w 
        return None 


def note(freq, len, amp=1000, rate=CD_RATE):
    t = np.linspace(0,len,len*rate)
    data = np.sin(2*np.pi*freq*t)*amp
    return data.astype(np.float32) # two byte integers
    
        
def rest_seconds(n): 
    r = Wave()
    samples=note(1, n, amp=0)  
    r.set(samples)  
    return r 
    
rest= rest_seconds(4) 


def test_init_set():
    a = Wave()
    d = np.array([1,2,3,4,5]) 
    a.set(d) 
    a2=a.samples
    assert np.array_equal(a2,d) 
    
def test_mix(): 
    a= Wave() 
    a.set(np.array([4,2,3]),rate=1)  
    a2 = a.copy() 
    
    b= Wave()
    b.set(np.array([2,2,2]),rate=1) 
    
    a.mix(b,1,cut=False)
    a.print() 
    
    c=Wave()
    c.set(np.array([4,4,5,2]), rate=1) 
    
    assert  a==c 
    
    a2.mix(b,1,cut=True)
    c2=Wave() 
    c2.set( np.array([4,4,5]), rate=1)
    
    assert np.array_equal(a2.samples, c2.samples) 
    
    
if __name__=='__main__': 
    test_mix() 


