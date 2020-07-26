import numpy as np
import wavio

fs = 44100  # sampling rate, Hz

duration = 10  # in seconds, may be float
f = 500.0  # sine frequency, Hz, may be float
volume = 0.5  # range [0.0, 1.0]

filename = 'output.wav'

# Generate a sample
samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs))

wavio.write(filename, samples, fs, sampwidth=3)  # Output a pure tone of the given freq
