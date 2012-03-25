#!/usr/bin/env python
#coding=utf8

"""
This module converts raw PCM values from files or standard input and saves
them to a WAV format file.

Currently the input and output formats must be the same.
"""

__author__ = "ToneGenerated"
__contact__ = "JonRuttan@gmail.com"
__copyright__ = "Copyright (C) 2012 Jon Ruttan"
__license__ = "Apache License, Version 2.0"
__version__ = "0.1.1"
__date__ = '2012-03-25'

import struct
import sys

class RawToWav:
    '''
    RawToWav([outfile=None, frame_rate=44100, channels=2, format='S16']) -> converter object

    Create a new converter object. This object can be used to convert
    input files sequentially.
    '''

    # The formats recognized by the converter (excluding shortcut formats)
    formats = {
        'U8': {'bits': 8, 'pack': 'b', 'label': 'Unsigned 8 bit'},
        'S16': {'bits': 16, 'pack': '<h', 'label': 'Signed 16 bit Little Endian'},
        'S32': {'bits': 32, 'pack': '<l', 'label': 'Signed 32 bit Little Endian'},
    }
    # The format shortcuts recognized by the converter
    format_shortcuts = {
        'CD': {'format': 'S16', 'frame_rate': 44100, 'channels': 2},
        'DAT': {'format': 'S16', 'frame_rate': 48000, 'channels': 2},
    }
    # The channels recognized by the converter
    channels = {
        1: 'Mono',
        2: 'Stereo',
        4: '4 Channel',
    }
    def __init__(self):
        '''
        Initializes converter object.
        '''
        # The outfile
        self.outfile = None
        self.frame_rate = None
        self.channels = None
        self.bits = None
        self.frame_bytes = None
        self.pack_string = None
        self.frames = None

    @staticmethod
    def parse_args(params):
        '''
        parse_args(params) -> params
        Parses converter object parameters for format and channel errors
        and converts format shortcuts.

        '''
        # Make the format parameter case insensitive
        params['format'] = params['format'].upper()

        # Apply shortcut formats
        if params['format'] in RawToWav.format_shortcuts.keys():
            params.update(RawToWav.format_shortcuts[params['format']])

        # Test the format parameter
        if params['format'] not in RawToWav.formats.keys():
            params['format'] = False

        # Test the channels parameter
        if params['channels'] not in RawToWav.channels.keys():
            params['channels'] = False

        return params

    def open(self, outfile, frame_rate=44100, channels=2, format='S16'):
        '''
        open(outfile, [frame_rate=44100, channels=2, format='S16']) -> converter object|False

        Opens a new file for output. Closes previously opened file.
        '''

        # Look up the format (assume the arguments may not have been parsed)
        try:
            format = RawToWav.formats[format.upper()]
        except:
            print 'Invalid format'
            return False

        # Look up the channels (assume the arguments may not have been parsed)
        if channels not in RawToWav.channels.keys():
            print 'Invalid channels'
            return False

        # Close any previously opened files
        if self.outfile is not None:
            self.close()

        # Open the outfile for writing
        self.outfile = open(outfile, "w")

        # Set the rest of the data attributes
        self.frame_rate = frame_rate
        self.channels = channels
        self.bits = format['bits']
        self.frame_bytes = channels * self.bits / 8
        self.pack_string = format['pack']
        self.frames = 0

        # Create the output file header
        self.outfile.write('RIFF')
        # This value will be updated when the update() method is called
        self.outfile.write(struct.pack('<L', 36))
        self.outfile.write('WAVE')
        self.outfile.write('fmt ')
        self.outfile.write(struct.pack('<L', 16))
        self.outfile.write(struct.pack('<H', 0x1))
        self.outfile.write(struct.pack('<H', self.channels))
        self.outfile.write(struct.pack('<L', self.frame_rate))
        self.outfile.write(struct.pack('<L', self.frame_rate * self.frame_bytes))
        self.outfile.write(struct.pack('<H', self.frame_bytes))
        self.outfile.write(struct.pack('<H', self.bits))
        self.outfile.write('data')
        # This value will be updated when the update() method is called
        self.outfile.write(struct.pack('<L', 0))
        return self

    def convert(self, infile):
        '''
        convert(infile) -> converter object

        Reads data from infile and writes it to the converter object outfile.
        '''

        # If the outfile is valid, cycle indefinitely
        while self.outfile != None:
            # Simple version, copy a frame from the input to the output
            frame = file.read(self.frame_bytes)
            if not len(frame):
                break
            self.outfile.write(frame)

            # Complex version, copy and convert samples to numeric entities
            # Could be used to modify each sample before it is written
#            # Cycle through each of the channels
#            for channel in range(0, self.channels):
#                # Try to read and convert the sample, return on error
#                try:
#                    datum = file.read(self.bits / 8)
#                    sample = struct.unpack(self.pack_string, datum)[0]
#                    self.outfile.write(struct.pack(self.pack_string, sample))
#                except:
#                    return self
            # Increment the number of frames processed
            self.frames += 1
        return self

    def update(self):
        '''
        update() -> converter object

        Updates the WAV file header.
        '''
        # If the outfile is valid, flush the file and update the RIFF headers
        if self.outfile is not None:
            self.outfile.flush()
            self.outfile.seek(4)
            self.outfile.write(struct.pack('<L', 36 + self.frames * self.frame_bytes))
            self.outfile.seek(40)
            self.outfile.write(struct.pack('<L', self.frames * self.frame_bytes))
        return self

    def close(self):
        '''
        close() -> converter object

        Updates the WAV file header and closes the converter object file.
        '''
        # If the outfile is valid, call the update method and close the file
        if self.outfile is not None:
            self.update()
            self.outfile.close()
        self.outfile = None
        return self


if __name__ == '__main__':

    # Import the argument parser
    import argparse

    # Create a command line argument parser
    parser = argparse.ArgumentParser(
            description='''Converts raw PCM FILE(s), or standard input, to OUTFILE file in WAV format.''',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''With no INFILE, or when INFILE is -, read standard input.

Recognized sample formats are: %s
The available format shortcuts are:
-f cd (16 bit little endian, 44100, stereo)
-f dat (16 bit little endian, 48000, stereo)
            ''' % ' '.join(sorted(RawToWav.formats.keys()))
        )
    # Outfile argument - takes one filename
    parser.add_argument('outfile', metavar='OUTFILE', type=str,
                        help='output file')
    # Optional INFILE argument - takes multiple filenames, '-' for standard
    # input, defaults to '-'
    parser.add_argument('infiles', metavar='INFILE', type=str, nargs='*', default='-',
                        help='input file')
    # Optional frame rate argument in Hz, defaults to 44100
    parser.add_argument('-r', '--rate', dest='frame_rate', type=int, default=44100,
                        required=False,
                        help='output frame rate.')
    # Optional channel argument, defaults to 2
    parser.add_argument('-c', '--channels', dest='channels', type=int, default=2,
                        required=False,
                        help='output channels')
    # Optional format argument, defaults to S16 (signed 16 bit integer)
    parser.add_argument('-f', '--format', dest='format', type=str, default='S16',
                        required=False,
                        help='sample format (case insenstive)')

    # Optional quiet flag, suppresses output information, defaults to None
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_const',
                        const=True, required=False,
                        help='quiet mode')

    # Version flag, outputs version information
    parser.add_argument('-V', '--version', action='version',
                       version='%s: version %s by %s <%s>' % \
                               (sys.argv[0], __version__, __author__, __contact__),
                       help='print current version')

    # Parse the supplied command line options
    args = parser.parse_args()

    # Filter the command line options that are to be parameters to the converter
    # object and store them in a dictionary
    params = { filtered_keys: vars(args)[filtered_keys] for filtered_keys in
            ('outfile', 'frame_rate', 'channels', 'format') }

    # Parse the parameter dictionary to ensure the values supplied are valid
    params = RawToWav.parse_args(params)

    # Test the value of the 'format' parameter, if false, it failed validation
    if not params['format']:
        print 'Invalid format:', args.format
        sys.exit(1)

    # Test the value of the 'channels' parameter, if false, it failed validation
    if not params['channels']:
        print 'Invalid channels:', args.channels
        sys.exit(1)

    # Give some feedback to the user, unless quiet mode is on
    if not args.quiet:
        print "Creating '%s': %s, Rate %d Hz, %s" % (params['outfile'],
                RawToWav.formats[params['format']]['label'],
                args.frame_rate,
                RawToWav.channels[params['channels']],
            )

    # Create the converter object with the parameters supplied
    converter = RawToWav().open(**params)

    # If the converter is False, something's gone wrong
    if not converter:
        sys.exit(1)

    # Cycle through the infiles, converting the data
    for infile in args.infiles:
        with infile == '-' and sys.stdin or open(infile, 'r') as file:
            converter.convert(file)

    # Close the converter object
    converter.close()

    # Give some more feedback to the user, unless quiet mode is on
    if not args.quiet:
        print 'Wrote', converter.frames, 'frames'
