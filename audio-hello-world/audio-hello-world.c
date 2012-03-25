/*
 * Copyright 2012 Jonathan Ruttan <JonRuttan@gmail.com>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 *
 * This program generates square waves as 16bit mono PCM samples and outputs
 * them to stdout.
 *
 * Due to rounding errors this code will only produce a close approximation
 * of the tone frequency specified. The deviation is inversely proportional
 * to the sampling rate.
 *
 *
 * @file		audio-hello-world.c
 * @author		ToneGenerated
 * @contact		JonRuttan@gmail.com
 * @copyright	Copyright (C) 2012 Jon Ruttan
 * @license		Apache License, Version 2.0
 * @version	0.1.0
 * @date		2012-03-18
 *
 */

#include <stdio.h>
#include <stdlib.h>

int gen_square_wave(int sample_rate, int frequency, int duration, float amplitude)
{
	/*
		Given the input parameters generates square waves and outputs them
		to stdout.

		Parameters:

		- `sample_rate`: The audio hardware's sampling rate in Hz
			(samples/sec.)
		- `frequency`: The square wave frequency in Hz (cycles/sec.)
		- `duration`: The duration of the square wave tone in ms.
		- `amplitude`: The amplitude of the square wave represented as a
			fraction of the maximum output volume.

	*/

	// Calculate the total number of samples required to produce a tone of
	// the duration specified.
	int samples = sample_rate * duration / 1000;

	// Calculate the number of samples in each half of the tone's cycle.
	int tone_midpoint = sample_rate / frequency / 2;

	// Calculate the maximum (negative) sample value.
	int sample = -(1 << (16 - 1)) * amplitude;

	// Iterate over the range of samples we've calculated are required.
	int i;
	for(i=0; i < samples; i++)
	{
		// Each time the iterator value reaches a half-cycle, change the
		// sample's sign, from the positive to the negative domain and
		// vice-versa.
		if(i % tone_midpoint == 0)
			sample = -sample;

		// Output the sample value to stdout as a little-endian 16bit integer
		printf("%c%c", sample & 0xff, (sample >> 8) & 0xff);
	}

	return 0;
}

int main(int argc, char *argv[])
{
	gen_square_wave(44100, 440, 1000, 0.3);
	return 0;
}
