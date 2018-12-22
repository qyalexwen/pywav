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
    
    def set(self, rate, samples): 
        self.rate = rate
        self.samples = samples 
    
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
        s2 /= m 
        self.samples = s2 
            
    def mix(self,start, end, wave2, ratio=1): 
        rate=self.rate 
        rate2=wave2.rate 
        w2=wave2.samples
        
        if rate != rate2: 
            print('Rate not match', rate2) 
            return None 
        start0 = int(rate * start) 
        end0 = int(rate * end) 
        len1 = end0 - start0 
        len2 = len(w2) 
        out=self.samples.copy() 
        if len1 < len2: # chord is too long, cut it 
            out[start0:end0] += w2[:len1]*ratio 
        else: 
            out[start0:start0+len2] += w2*ratio 
        # out /= 2.0
        oc = Wave()
        oc.set(self.rate, out) 
        return oc
        
    def mul(self, rate): 
        self.samples = self.samples * rate 
    
    def imul(self, other): 
        self.mul(other) 
 
    def __truediv__(self, other): 
        n = int( self.rate * 60 *4 / ( self._tempo * other)) 
        a = Wave()
        a.set( self.rate, self.samples[:n]  ) 
        return a 
        
    def save(self, filename): 
        self.normalize() 
        wf.write( filename, self.rate, self.samples) 

    def __add__(self, w2): 
        if self.rate != w2.rate: 
            print("Rates don't match", self.rate, w2.rate) 
            return None 
        else: 
            samples = np.concatenate([ self.samples, w2.samples] ) 
            c = Wave()
            c.set(self.rate, samples) 
            return c
    
    def piece(self, start, end): 
        rate=self.rate 
        start0 = int(rate * start) 
        end0 = int(rate * end) 
        oc=Wave() 
        oc.set(rate, self.samples[start0:end0]) 
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
            w.set(self.rate, samples)
            return w 
        return None 


def note(freq, len, amp=1000, rate=CD_RATE):
    t = np.linspace(0,len,len*rate)
    data = np.sin(2*np.pi*freq*t)*amp
    return data.astype(np.float32) # two byte integers
    
        
_rest0 = note(1, 4, amp=0, rate=CD_RATE) 

rest=Wave()
rest.set(CD_RATE, _rest0) 


def test_init_set():
    a = Wave()
    d = np.array([1,2,3,4,5]) 
    a.set(44100, d) 
    a2=a.samples
    assert a2==d 
    



