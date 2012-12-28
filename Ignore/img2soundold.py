from Ignore import mineFft

__author__ = 'liuc'


import scipy
import wave,struct,numpy
import Image

MAX_VOLUME=0.8

my_wave=wave.open('1000.wav')
NumChannel = my_wave.getnchannels()
NumSampWidth = my_wave.getsampwidth()
SampFreq = my_wave.getframerate()
NumFrames = my_wave.getnframes()
Duration = NumFrames*1/SampFreq

FrameSez = int(0.08 * SampFreq)
FrameHop = int(0.05 * SampFreq)

data = my_wave.readframes(NumFrames)

print "TypeSound: " , type(data)," NumChannel: ",NumChannel, " Samples Size: ", NumSampWidth, " Frequency: ", SampFreq, " NumFrames: " , NumFrames

data_unpack = numpy.frombuffer(data,'i2')

data_fft=[]
start=0

# Calc FFT
while start < NumFrames - FrameSez:
    data_fft.append(mineFft.fft(data_unpack[start:start+FrameSez]))
    start+=FrameHop

if (start+FrameSez <> NumFrames):
    data_fft.append(mineFft.fft(data_unpack[start:]))


data_tmp=(data_fft[0])
#data_real=scipy.real(data_tmp)
#data_imag=scipy.imag(data_tmp)

#pylab.plot(data_real)
#pylab.plot(data_imag)

#pylab.show()

data_fft=[]
data_fft.append(data_tmp)


# Calc IFFt
#sound_pack=''
#sound_ifft=scipy.zeros(2205)#NumFrames)
#start=0
#
#for sound_fft in data_fft:
#    print len(sound_fft)," ",FrameSez," ", start+FrameSez," ", 678258
#    #sound_ifft[start:start+FrameSez] += mineFft.ifft(sound_fft)
#    sound_ifft[0:0+2205]=mineFft.ifft(sound_fft)
#    start+=FrameHop



#print start," ", NumFrames," ", FrameHop, " ", FrameSez, " ", max(sound_ifft), " ", min(sound_ifft)
#max_sound=max(sound_ifft)
#min_sound=min(sound_ifft)
#sound_ifft=MAX_VOLUME*((sound_ifft/max_sound)*32760)

pi=3.1415
freq=700
w = scipy.hamming(FrameSez)

t_scale = scipy.linspace(0,1.0*FrameSez/SampFreq, num=FrameSez)

my_wave=wave.open('bird.wav')
dataBird = my_wave.readframes(my_wave.getnframes())
dataBirdu = numpy.frombuffer(dataBird,'i2')

imgIn = Image.open('images3.jpg').convert("L")
imgIn_size =imgIn.size
imgMat = numpy.array(imgIn.getdata()).reshape(imgIn_size[1],imgIn_size[0]).tolist()

if dataBirdu.size > FrameHop*imgIn_size[1]+FrameSez:
    sound_out=numpy.zeros(dataBirdu.size) #
else:
    sound_out=numpy.zeros(FrameHop*imgIn_size[1]+FrameSez)

sound_out[0:dataBirdu.size]=255.0*dataBirdu/max(dataBirdu)

n=0
m_log=numpy.log2(scipy.linspace(1.01,2,num=imgIn_size[0]))
MAX_FREQ=12000

for line in imgMat:
    m=0
    for element in line:
        sound_out[n*FrameHop:n*FrameHop+FrameSez]+=(w**2)*(50/(m_log[m]))*((element/255.0)**3)*numpy.sin(2*pi*t_scale*MAX_FREQ*m_log[m])
        m+=1
    print "next line"
    n+=1

maxSound=max(abs((sound_out)))
sound_out = 32000*(sound_out)/maxSound

print min(sound_out)
print max(sound_out)
sound_pack=''
for i in sound_out:
    sound_pack+=struct.pack('h',i)



out_wave = wave.open('out.wav','w')
out_wave.setnchannels(NumChannel)
out_wave.setsampwidth(NumSampWidth)
out_wave.setframerate(SampFreq)
out_wave.writeframes(sound_pack)
out_wave.close()


#data_fft=data_fft[0]
#f_scale = scipy.linspace(0,SampFreq/2,num=FrameSez/2)
#print "LenFrameSez: ", FrameSez, " LenFFT: ", len(data_fft), " FScale: ", len(f_scale)



#print "LenSound: ", len(sound_ifft), " TypeIFFT: ", type(sound_ifft)




#pylab.plot(f_scale,abs(data_fft[0:FrameSez/2]))

#pylab.show()