**ToneGenerated** is a blog devoted to audio programming, it is located at
<http://tonegenerated.wordpress.com/>

**ToneGenerated** is a blog for computer audio enthusiasts, which explores the
development of computer code for sound and music synthesis, and manipulation.
Follow along to build and dissect a host of sound-related projects; from the
trivial to the advanced--**ToneGenerated** does the heavy-lifting.

The development environment we're using is
[GNU/Linux](http://en.wikipedia.org/wiki/Linux), specifically
[Ubuntu](http://www.ubuntu.com/), but the code is targeted at a general
audience, and should only require small changes to run on Windows, Mac,
smartphones, tablets and microcontrollers.

Most of the code is in the
[C programming language](http://en.wikipedia.org/wiki/C_(programming_language),
both for the speed of the binaries it generates, and its availability on
most platforms...but the code is written to be easily ported to other languages.
ToneGenerated's mantra is: *keep it simple, portable and well documented*.

The [Python programming language](http://www.python.org/) is used for
prototyping, scripting and some visualization routines.

A few of the projects use the
[Simple DirectMedia Layer(SDL)](http://www.libsdl.org/) cross-platform
multimedia libraries, but none of the techniques explored rely on its
availability on the system you're developing for. As long as you can get
the system to output [PCM](http://en.wikipedia.org/wiki/PCM)
samples--or even just play [WAV](http://en.wikipedia.org/wiki/WAV) files--
much of the code explored will be applicable.

**ToneGenerated** explores:

*  audio playback
*  tone generation
*  sound file format encoding and decoding (WAV/MIDI/MOD/SID/MP3/etc.)
*  visualization
*  sequencing
*  instruments and envelopes
*  sound effects
*  compression
*  ffts and spectrum analysis
*  speech synthesis
*  voiceprints
*  3D spatialization
