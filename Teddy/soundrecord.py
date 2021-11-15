import sounddevice as sd
import soundfile as sf

fs = 16000 # Sample rate
duration = 3 # Duration of recording

myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

sd.wait() # Wait until recording is finished
sf.write('output2.wav', myrecording, fs) # Save as WAV file 
