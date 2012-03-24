#!/usr/bin/env python
#coding=utf8

"""
This module converts raw PCM values from files or standard input and saves
them to a WAV format file.

"""

__author__ = "ToneGenerated"
__contact__ = "JonRuttan@gmail.com"
__copyright__ = "Copyright (C) 2012 Jon Ruttan"
__license__ = "Apache License, Version 2.0"
__version__ = "0.1.0"
__date__ = '2012-03-24'

import struct
import sys
import argparse

class RawToWav:
    '''
    RawToWav([outfile=None, frame_rate=44100, channels=2, format='S16']) -> converter object

    Create a new converter object. This object can be used to convert
    input files sequentially.
    '''
    formats = {
        'U8': {'bits': 8, 'pack': 'b', 'label': 'Unsigned 8 bit'},
        'S16': {'bits': 16, 'pack': '<h', 'label': 'Signed 16 bit Little Endian'},
        'S32': {'bits': 32, 'pack': '<l', 'label': 'Signed 32 bit Little Endian'},
    }
    channels = {
        1: 'Mono',
        2: 'Stereo',
        4: '4 Channel'
    }
    def __init__(self, outfile=None, frame_rate=44100, channels=2, format='S16'):
        '''
        Initializes object, see open() method.
        '''
        self.outfile = None
        if outfile is not None and not self.open(outfile, frame_rate, channels, format):
            self.outfile.close()

    @staticmethod
    def parse_args(params):
        '''
        parse_args(params) -> params
        Parses converter object parameters for format and channel errors
        and converts format shortcuts.

        '''
        params['format'] = params['format'].upper()
        if params['format'] == 'cd':
            params['format'] = 'S16'
            params['frame_rate'] = 44100
            params['channels'] =2
        elif params['format'] == 'dat':
            params['format'] = 'S16'
            params['frame_rate'] = 48000
            params['channels'] =2
        elif params['format'] not in RawToWav.formats.keys():
            params['format'] = False

        if params['channels'] not in RawToWav.channels.keys():
            params['channels'] = False

        return params

    def open(self, outfile, frame_rate=44100, channels=2, format='S16'):
        '''
        open(outfile, [frame_rate=44100, channels=2, format='S16']) -> converter object|False

        Opens a new file for output. Closes previously opened file.
        '''
        try:
            self.bits = RawToWav.formats[format]['bits']
        except:
            print 'Invalid format'
            return False
        if channels not in RawToWav.channels.keys():
            print 'Invalid channels'
            return False

        if self.outfile is not None:
            self.close()
        self.outfile = open(outfile, "w")
        self.frame_rate = frame_rate
        self.channels = channels
        self.frame_bytes = channels * self.bits / 8
        self.pack_string = RawToWav.formats[format]['pack']
        self.frames = 0

        self.outfile.write('RIFF')
        # This value will be updated when the closed() method is called
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
        # This value will be updated when the closed() method is called
        self.outfile.write(struct.pack('<L', 0))
        return self

    def convert(self, infile):
        '''
        convert(infile) -> converter object

        Reads data from infile and writes it to the converter object outfile.
        '''
        while self.outfile != False:
            for channel in range(0, self.channels):
                try:
                    datum = file.read(self.bits / 8)
                    sample = struct.unpack(self.pack_string, datum)[0]
                    self.outfile.write(struct.pack(self.pack_string, sample))
                    self.frames += 1
                except:
                    return False
        return self

    def close(self):
        '''
        close() -> converter object

        Updates the WAV file header and closes the converter object file.
        '''
        if self.outfile is not None:
            self.outfile.seek(4)
            self.outfile.write(struct.pack('<L', 36 + self.frames * self.frame_bytes))
            self.outfile.seek(40)
            self.outfile.write(struct.pack('<L', self.frames * self.frame_bytes))
            self.outfile.close()
        self.outfile = None
        return self


if __name__ == '__main__':
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
    parser.add_argument('outfile', metavar='OUTFILE', type=str,
                       help='output file')
    parser.add_argument('infiles', metavar='INFILE', type=str, nargs='*', default='-',
                       help='input file')
    parser.add_argument('-r', '--rate', dest='frame_rate', type=int, default=44100,
                       required=False,
                       help='output frame rate.')
    parser.add_argument('-c', '--channels', dest='channels', type=int, default=2,
                       required=False,
                       help='output channels')
    parser.add_argument('-f', '--format', dest='format', type=str, default='S16',
                       required=False,
                       help='sample format (case insenstive)')

    parser.add_argument('-q', '--quiet', dest='quiet', action='store_const', const=True,
                       required=False,
                       help='quiet mode')

    parser.add_argument('-V', '--version', action='version',
                       version='%s: version %s by %s <%s>' % \
                               (sys.argv[0], __version__, __author__, __contact__),
                       help='print current version')

    args = parser.parse_args()
    params = { filtered_keys: vars(args)[filtered_keys] for filtered_keys in
            ('outfile', 'frame_rate', 'channels', 'format') }

    params = RawToWav.parse_args(params)
    if not params['format']:
        print 'Invalid format:', args.format
        sys.exit(1)
    if not params['channels']:
        print 'Invalid channels:', args.channels
        sys.exit(1)

    if not args.quiet:
        print "Creating '%s': %s, Rate %d Hz, %s" % (params['outfile'],
                RawToWav.formats[params['format']]['label'],
                args.frame_rate,
                RawToWav.channels[params['channels']],
            )

    converter = RawToWav(**params)

    if converter.outfile is None:
        sys.exit(1)
    for infile in args.infiles:
        with infile == '-' and sys.stdin or open(infile, 'r') as file:
            converter.convert(file)

    converter.close()

    if not args.quiet:
        print 'Wrote', converter.frames, 'frames'
