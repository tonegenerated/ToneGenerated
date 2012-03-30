/*
 * Copyright 2012 Jonathan Ruttan <JonRuttan@gmail.com>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *	 http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 *
 * This module generates sine, square, triangle and sawtooth waves as 16bit
 * mono PCM samples and outputs them to the standard output.
 *
 *
 * @file		waveforms.c
 * @author		ToneGenerated
 * @contact		JonRuttan@gmail.com
 * @copyright	Copyright (C) 2012 Jon Ruttan
 * @license		Apache License, Version 2.0
 * @version	0.1.0
 * @date		2012-03-30
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/*
 * waveform_type structure type
 *
 * Storage for waveform structure type.
 */
typedef struct waveform_struct {
	int sample_rate;
} waveform_type;

/*
 * waveform(waveform_type, sample_rate) -> waveform_type
 *
 * Initializes values for waveform structure type.
 */
waveform_type *waveform_init(waveform_type *waveform, int sample_rate)
{
	waveform->sample_rate = sample_rate;
	return waveform;
}

/*
 * wavgen_type function pointer type
 *
 * Generator function prototype pointer
 */
typedef double (wavegen_type(double time));

/*
 * Generates individual sine wave samples.
 *
 * Parameters:
 * - `time` is a floating point value between 0.0 and 1.0.
 *
 * Returns a floating point value between -1.0 and 1.0.
 */
double wavegen_sine(double time)
{
	return sin(2.0 * M_PI * time);
}

/*
 * Generates individual triangle wave samples.
 *
 * Parameters:
 * - `time` is a floating point value between 0.0 and 1.0.
 *
 * Returns a floating point value between -1.0 and 1.0.
 */
double wavegen_triangle(double time)
{
	return 4.0 * (time - floor(time + 0.5)) * pow(-1, floor(time + 0.5)) - 1.0;
}

/*
 * Generates individual sawtooth wave samples.
 *
 * Parameters:
 * - `time` is a floating point value between 0.0 and 1.0.
 *
 * Returns a floating point value between -1.0 and 1.0.
 */
double wavegen_sawtooth(double time)
{
	return 2.0 * (time - floor(time)) - 1.0;
}

/*
 * Generates individual square wave samples.
 *
 * Parameters:
 * - `time` is a floating point value between 0.0 and 1.0.
 *
 * Returns a floating point value between -1.0 and 1.0.
 */
double wavegen_square(double time)
{
	double duty = 0.5;
	return wavegen_sawtooth(time) - wavegen_sawtooth(time - duty);
}

/*
 * Given the input parameters generates waves and outputs them
 * to stdout.
 *
 * Parameters:
 * - `waveform`: A pointer to the waveform structure to operate on.
 * - `wavegen`: A pointer to the wavegen function which will generate samples.
 * - `frequency`: The wave frequency in Hz (cycles/sec.)
 * - `duration`: The duration of the wave tone in ms.
 * - `amplitude`: The amplitude of the wave represented as a fraction
 * 	of the maximum output volume.
 *
 * Returns the waveform struct.
 */
waveform_type *waveform_gen_wave(waveform_type *waveform, wavegen_type *wavegen,
	int frequency, int duration, double amplitude)
{
	// Calculate the total number of samples required to produce a tone of
	// the duration specified.
	int samples = waveform->sample_rate * duration / 1000;

	// Calculate the number of samples in a full tone cycle
	double tone_width = (double)(waveform->sample_rate) / frequency;

	// Calculate the maximum (negative) sample value.
	int max_sample = (1 << (16 - 1)) * amplitude;

	// Iterate over the range of samples we've calculated are required.
	int i, sample;
	for(i=0; i < samples; i++)
	{
		// Calculate the sample value
		sample = wavegen(fmod(i, tone_width) / tone_width) * max_sample;

		// Output the sample value to stdout as a little-endian 16bit integer
		fputc(sample & 0xff, stdout);
		fputc((sample >> 8) & 0xff, stdout);
	}

	return waveform;
}

int main(int argc, char *argv[])
{
	// Create storage for our waveform structure type
	waveform_type waveform;

	// Initialize the waveform structure type
	waveform_init(&waveform, 44100);

	// Generate a wave of each type
	waveform_gen_wave(&waveform, &wavegen_sine, 440, 1000, 0.3);
	waveform_gen_wave(&waveform, &wavegen_triangle, 440, 1000, 0.3);
	waveform_gen_wave(&waveform, &wavegen_sawtooth, 440, 1000, 0.3);
	waveform_gen_wave(&waveform, &wavegen_square, 440, 1000, 0.3);

	return 0;
}
