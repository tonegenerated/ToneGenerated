#!/usr/bin/env python

"""
This module generates square waves as 16bit mono PCM samples and outputs
them to stdout.

Due to rounding errors this code will only produce a close approximation
of the tone frequency specified. The deviation is inversly proportional to
the sampling rate.

"""

__application__ = "audio-hello-world.py"
__author__ = "ToneGenerated"
__contact__ = "JonRuttan@gmail.com"
__copyright__ = "Copyright (C) 2012 Jon Ruttan"
__license__ = "Apache License, Version 2.0"
__version__ = "0.1.0"
__date__ = '2012-03-18'

import struct
import sys

def gen_square_wave(sample_rate=44100, frequency=440, duration=1000, amplitude=0.3):
    """Given the input parameters generates square waves and outputs them
    to stdout.

    Parameters:

    - `sample_rate`: The audio hardware's sampling rate in Hz (samples/sec.)
    - `frequency`: The square wave frequency in Hz (cycles/sec.)
    - `duration`: The duration of the square wave tone in ms.
    - `amplitude`: The amplitude of the square wave represented as a fraction
        of the maximum output volume.

    """
    # Calculate the total number of samples required to produce a tone of
    # the duration specified.
    samples = sample_rate * duration / 1000

    # Calculate the number of samples in each half of the tone's cycle.
    tone_midpoint = sample_rate / frequency / 2

    # Calculate the maximum (negative) sample value.
    sample = -(1 << (16 - 1)) * amplitude

    # Iterate over the range of samples we've calculated are required.
    for i in range(0, samples):
        # Each time the iterator value reaches a half-cycle, change the sample's
        # sign, from the positive to the negative domain and vice-versa.
        if i % tone_midpoint == 0:
            sample = -sample

        # Output the sample value to stdout as a little-endian 16bit integer
        sys.stdout.write(struct.pack('<l', sample))


if __name__ == '__main__':
    gen_square_wave(44100, 440, 1000, 0.3)
