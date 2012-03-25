#!/usr/bin/env python
# coding=utf8

# Copyright 2012 Jonathan Ruttan <JonRuttan@gmail.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


"""
This module generates sine, square, triangle and sawtooth waves as 16bit
mono PCM samples and outputs them to the standard output.

"""

__application__ = "waveforms.py"
__author__ = "ToneGenerated"
__contact__ = "JonRuttan@gmail.com"
__copyright__ = "Copyright (C) 2012 Jonathan Ruttan"
__license__ = "Apache License, Version 2.0"
__version__ = "0.1.0"
__date__ = '2012-03-25'

import struct
import sys
from math import *

class Waveform:
    def __init__(self):
        '''
        Creates new waveform object.
        '''
        self.sample_rate = None

    def waveform(self, sample_rate=44100):
        '''
        waveform([sample_rate=44100]) -> converter object

        Initializes values for waveform object.
        '''
        self.sample_rate = sample_rate
        return self

    @staticmethod
    def sine(time):
        '''
        Generates individual sine wave samples.

        Parameters:
        - `time` is a floating point value between 0.0 and 1.0.

        Returns a floating point value between 0.0 and 1.0.
        '''
        return sin(2 * pi * time)

    @staticmethod
    def triangle(time):
        '''
        Generates individual triangle wave samples.

        Parameters:
        - `time` is a floating point value between 0.0 and 1.0.

        Returns a floating point value between 0.0 and 1.0.
        '''
        return (time - 2 * floor((time + 1) /2)) * pow(-1, floor((time + 1) /2))

    @staticmethod
    def sawtooth(time):
        '''
        Generates individual sawtooth wave samples.

        Parameters:
        - `time` is a floating point value between 0.0 and 1.0.

        Returns a floating point value between 0.0 and 1.0.
        '''
        return 2 * (time - floor(time)) - 1

    @staticmethod
    def square(time, duty=0.5):
        '''
        Generates individual square wave samples.

        Parameters:
        - `time` is a floating point value between 0.0 and 1.0.
        - `duty` is a floating point value between 0.0 and 1.0.

        Returns a floating point value between 0.0 and 1.0.
        '''
        return Waveform.sawtooth(time) - Waveform.sawtooth(time - duty)

    def gen_wave(self, waveform, frequency=440, duration=1000, amplitude=0.3):
        """Given the input parameters generates waves and outputs them
        to stdout.

        Parameters:

        - `frequency`: The wave frequency in Hz (cycles/sec.)
        - `duration`: The duration of the wave tone in ms.
        - `amplitude`: The amplitude of the wave represented as a fraction
            of the maximum output volume.

        """
        # Calculate the total number of samples required to produce a tone of
        # the duration specified
        samples = self.sample_rate * duration / 1000

        # Calculate the number of samples in a full tone cycle
        tone_width = float(self.sample_rate) / frequency

        # Calculate the maximum sample value
        max_sample = (1 << (16 - 1)) * amplitude

        # Iterate over the range of samples we've calculated are required
        for i in range(0, samples):
            # Calculate the sample value
            sample = waveform(i % tone_width / tone_width) * max_sample

            # Output the sample value to stdout as a little-endian 16bit integer
            sys.stdout.write(struct.pack('<h', sample))

        return self

if __name__ == '__main__':
    # Create an instance of the Waveform class
    waveform = Waveform().waveform(44100)

    # Generate a wave of each type
    waveform.gen_wave(Waveform.sine, 440, 1000, 0.3)
    waveform.gen_wave(Waveform.triangle, 440, 1000, 0.3)
    waveform.gen_wave(Waveform.sawtooth, 440, 1000, 0.3)
    waveform.gen_wave(Waveform.square, 440, 1000, 0.3)
