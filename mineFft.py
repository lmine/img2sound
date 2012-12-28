__author__ = 'liuc'
import scipy


def fft(data):
    w = scipy.hamming(len(data))
    return scipy.fft(w*data)

def ifft(data):
    return scipy.real(scipy.ifft(data))
