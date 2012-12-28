__author__ = 'liuc'

import scipy, wave,struct,numpy
import Image, math

def img2sound(imageData, maxFrequency, maxVolume, sampleFrequency, windowHop, windowLength, scale):
    imgIn_size = imageData.size
    imgInMatrix = numpy.array(imageData.getdata()).reshape(imgIn_size[1],imgIn_size[0]).tolist()

    windowStep = int(windowHop * sampleFrequency)
    windowSize = int(windowLength * sampleFrequency)
    soundOutSize = imgIn_size[1]*windowStep+windowSize

    soundOutData=numpy.zeros(soundOutSize)

    tScale = scipy.linspace(0,1.0*windowSize/sampleFrequency, num=windowSize)
    if scale=='log':
        fScale = 10**(scipy.linspace(-2,0,num=imgIn_size[0])) #logaritihm scale
    elif scale=='linear':
        fScale = scipy.linspace(0,1,num=imgIn_size[0]) #linear scale
    else:
        print "Wrong scale!"
        raise

    magResponse = (1-fScale)

    w = scipy.hamming(windowSize)

    n=0
    for line in imgInMatrix:
        m=0
        for element in line:
            soundOutData[n:n+windowSize]+=w*magResponse[m]*(element/255.0)*numpy.sin(2*math.pi*tScale*fScale[m]*maxFrequency)
            m+=1
        n+=windowStep

    maxOutSound=max(abs(soundOutData))

    soundOutData = maxVolume * 32767 * (soundOutData)/(maxOutSound)

    soundOutDataPack=''
    for val in soundOutData:
        soundOutDataPack+=struct.pack('h',val)

    return soundOutDataPack

def main():

#    soundIn=wave.open('bird.wav')
#    NumChannel = soundIn.getnchannels()
#    NumSampWidth = soundIn.getsampwidth()
#    SampFreq = soundIn.getframerate()
#    NumFrames = soundIn.getnframes()
#
#    Duration = NumFrames*1/SampFreq
#
#    print NumSampWidth," ", SampFreq," ", NumChannel
#
#    soundInData = soundIn.readframes(NumFrames)
#    soundInDataUnpack = numpy.frombuffer(soundInData,'i2')

    imgIn = Image.open('images1.jpg').convert("L")

    soundOutDataPack = img2sound(imgIn, 15000, 0.5, 44100, 0.06, 0.1, 'log')


    soundOut = wave.open('out.wav','w')
    soundOut.setnchannels(1)
    soundOut.setsampwidth(2)
    soundOut.setframerate(44100)

    soundOut.writeframes(soundOutDataPack)

    soundOut.close()


main()