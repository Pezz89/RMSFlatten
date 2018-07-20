#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdb
import argparse
from pysndfile import PySndfile

from pathtype import PathType
import csv

def flattenRMS(AudioFile, AnnotationFile):
    with open(AnnotationFile, 'r') as f:
        csvReader = csv.reader(f)
        lines = []
        for line in csvReader:
            lines.append(line)
        pdb.set_trace()


if __name__ == "__main__":
    # Create commandline interface
    parser = argparse.ArgumentParser(description='Generate stimulus for '
                                     'training TRF decoder by concatenating '
                                     'matrix test materials')
    parser.add_argument('AudioFile', type=PathType(exists=True),
                        default='./speech.wav',
                        help='Speech wave file')
    parser.add_argument('AnnotationFile', type=PathType(exists=True),
                        default='./speech.csv', help='Speech annotatin csv')
    args = {k:v for k,v in vars(parser.parse_args()).items() if v is not None}


    # Generate stimulus from arguments provided on command line
    flattenRMS(**args)
