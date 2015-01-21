#!/usr/bin/env python
# CREATED:2013-03-08 15:25:18 by Brian McFee <brm2132@columbia.edu>
#  unit tests for librosa.feature (feature.py)
#
# Run me as follows:
#   cd tests/
#   nosetests -v
#
# This test suite verifies that librosa core routines match (numerically) the output
# of various DPWE matlab implementations on a broad range of input parameters.
#
# All test data is generated by the Matlab script "makeTestData.m".
# Each test loads in a .mat file which contains the input and desired output for a given
# function.  The test then runs the librosa implementation and verifies the results
# against the desired output, typically via numpy.allclose().
#
# CAVEATS:
#
#   Currently, not all tests are exhaustive in parameter space.  This is typically due
#   restricted functionality of the librosa implementations.  Similarly, there is no
#   fuzz-testing here, so behavior on invalid inputs is not yet well-defined.
#

# Disable cache
import os
try:
    os.environ.pop('LIBROSA_CACHE_DIR')
except:
    pass

import librosa
import glob
import numpy
import scipy.io


#-- utilities --#
def files(pattern):
    test_files = glob.glob(pattern)
    test_files.sort()
    return test_files

def load(infile):
    DATA = scipy.io.loadmat(infile, chars_as_strings=True)
    return DATA
#--           --#


#-- Tests     --#
def test_hz_to_mel():
    def __test_to_mel(infile):
        DATA = load(infile)
        z = librosa.hz_to_mel(DATA['f'], DATA['htk'])

        assert numpy.allclose(z, DATA['result'])

    for infile in files('data/feature-hz_to_mel-*.mat'):
        yield (__test_to_mel, infile)

    pass


def test_mel_to_hz():

    def __test_to_hz(infile):
        DATA = load(infile)
        z = librosa.mel_to_hz(DATA['f'], DATA['htk'])

        assert numpy.allclose(z, DATA['result'])

    for infile in files('data/feature-mel_to_hz-*.mat'):
        yield (__test_to_hz, infile)

    pass


def test_hz_to_octs():
    def __test_to_octs(infile):
        DATA = load(infile)
        z = librosa.hz_to_octs(DATA['f'])

        assert numpy.allclose(z, DATA['result'])

    for infile in files('data/feature-hz_to_octs-*.mat'):
        yield (__test_to_octs, infile)

    pass


def test_melfb():

    def __test(infile):
        DATA = load(infile)

        wts = librosa.filters.mel(DATA['sr'][0],
                                  DATA['nfft'][0],
                                  n_mels=DATA['nfilts'][0],
                                  fmin=DATA['fmin'][0],
                                  fmax=DATA['fmax'][0],
                                  htk=DATA['htk'][0])

        # Our version only returns the real-valued part.
        # Pad out.
        wts = numpy.pad(wts, [(0, 0),
                              (0, int(DATA['nfft'][0]/2 - 1))],
                        mode='constant')

        assert wts.shape == DATA['wts'].shape

        assert numpy.allclose(wts, DATA['wts'])

    for infile in files('data/feature-melfb-*.mat'):
        yield (__test, infile)
    pass


def test_chromafb():

    def __test(infile):
        DATA = load(infile)

        octwidth = DATA['octwidth'][0, 0]
        if octwidth == 0:
            octwidth = None

        wts = librosa.filters.chroma(DATA['sr'][0, 0],
                                     DATA['nfft'][0, 0],
                                     DATA['nchroma'][0, 0],
                                     A440=DATA['a440'][0, 0],
                                     ctroct=DATA['ctroct'][0, 0],
                                     octwidth=octwidth)

        # Our version only returns the real-valued part.
        # Pad out.
        wts = numpy.pad(wts, [(0, 0),
                              (0, int(DATA['nfft'][0, 0]/2 - 1))],
                        mode='constant')

        assert wts.shape == DATA['wts'].shape

        assert numpy.allclose(wts, DATA['wts'])

    for infile in files('data/feature-chromafb-*.mat'):
        yield (__test, infile)
    pass