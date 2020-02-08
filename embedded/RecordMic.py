

import pyaudio
import wave
import os
import threading
import numpy

VOLUME_THRESHOLD = 80

class Microphone(): 
    def __init__(self, verbose = 0, record_secs = 3): 
        self.verbose = verbose
        self.format = pyaudio.paInt16
        self.channel_number = 1
        self.samp_rate = 44100
        self.chunk = 4096
        self.dev_index = 2
        self.wav_output_filename = 'record_{}.wav'
        self.record_counter = 0
        self.THRESHOLD_SILENCE = 100

    def is_talking(self): 
        """ Records a 4 seconds clips
            Returns 1 if max volume of sound data is above set threshold.
            Input: array containing sound data
            Output: 1 if max volume is above set threshold. 
        """
        volume = self.get_volume()
        if self.verbose: 
            print("volume: ", volume)
        if volume > VOLUME_THRESHOLD: 
            return False
        return True

    def get_volume(self): 
        """ Returns maximum volume during the recording. 
            Input : array containing sound data
            Output: non-normalised maximum volume of clip
        """
        self.record(3)
        decoded = numpy.frombuffer(max(self._frames), numpy.int16)
        return max(numpy.absolute(decoded))


    def record(self, record_secs): 
        """ Records audio stream 
            Input: number of seconds of the recording
            Output: None. Changes the class attribute self.stream
        """
        self.audio = pyaudio.PyAudio()

        try: 
            self.stream= self.audio.open(
                format = self.format,
                rate=self.samp_rate,
                channels=self.channel_number, 
                input_device_index = self.dev_index, 
                input=True, 
                frames_per_buffer=self.chunk)

            if self.verbose: 
                print("Recording for {} ...".format(record_secs))
        
        except Exception as e: 
            print(e)

        self._frames=[]
        _chunk_number = int((self.samp_rate/self.chunk)*record_secs)

        for ii in range(0,_chunk_number):
            data=self.stream.read(self.chunk, exception_on_overflow = False)
            self._frames.append(data)

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()  

        if self.verbose: 
            print("finished recording")

    def record_to_file(self, record_secs):
        """ Records an audio and saves it to a .wav file
            Input: number of seconds of the recording
            Output: saved .wav file
        """
        self.record(record_secs) 
        self._generate_wav_file()
        self.record_counter += 1

    def _generate_wav_file(self): 
        """ Creates a .wav file from the an audio stream with filename record_#.wav
            Input: audio stream from class attribute
            Output: saved .wav file with record_#.wav filename
        """
        file_number = self.record_counter%5 
        wavefile=wave.open(self.wav_output_filename.format(file_number),'wb')
        wavefile.setnchannels(self.channel_number)
        wavefile.setsampwidth(self.audio.get_sample_size(self.format))
        wavefile.setframerate(self.samp_rate)
        wavefile.writeframes(b''.join(self._frames))
        wavefile.close()

if __name__ == "__main__":
    mic = Microphone(verbose=1)
    while True: 
        print(mic.is_talking())
