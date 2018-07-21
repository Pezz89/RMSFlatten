#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdb
import argparse
from pysndfile import sndio

from pathtype import PathType
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def flattenRMS(AudioFile, AnnotationFile):
    with open(AnnotationFile, 'r') as f:
        csvData = pd.read_csv(f)
    data, fs, encStr, fmtStr = sndio.read(AudioFile, return_format=True)
    csvData['start'] *= fs
    csvData['start'] = csvData['start'].astype(int)
    csvData['stop'] *= fs
    csvData['stop'] = csvData['stop'].astype(int)

    zerox = np.where(np.diff(np.sign(data)))[0]
    # get silent sections
    silences = csvData.loc[csvData['name'] == '#']
    audio = csvData.loc[csvData['name'] != '#']

    # Find nearest zero-crossing to start and stop times of silences
    nearestZerox = zerox[np.abs(zerox - csvData['start'][:, np.newaxis]).argmin(axis=1)]
    csvData['start'] = nearestZerox
    nearestZerox = zerox[np.abs(zerox - csvData['stop'][:, np.newaxis]).argmin(axis=1)]
    csvData['stop'] = nearestZerox

    csvData['rms'] = np.nan
    for ind, chunk in csvData.iterrows():
        if not chunk['name'] == '#':
            rms = np.sqrt(np.mean(data[chunk['start']:chunk['stop']]**2))
            csvData.iloc[ind, csvData.columns.get_loc('rms')] = rms
    avgRMS = csvData['rms'][csvData['rms'].notnull()].mean()

    silentData = np.zeros(int(0.3*fs))
    out = np.array([])
    for ind, chunk in csvData.iterrows():
        if chunk['name'] == '#':
            out = np.append(out, silentData)
        else:
            rmsCorFactor = avgRMS / chunk['rms']

            out = np.append(out, data[chunk['start']:chunk['stop']])#*rmsCorFactor)
            print(np.sqrt(np.mean((data[chunk['start']:chunk['stop']]*rmsCorFactor)**2)))

    sndio.write('./out.wav', out, rate=fs, format=fmtStr, enc=encStr)



    #silences['start'] = np.abs(zerox - silences['start'])).min()


    #for line in lines[1:]:




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
