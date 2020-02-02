
import pyaudio
import wave
import os

class microphone(): 
    def __init__(self, verbose = 0, record_secs = 3): 
        self.verbose = verbose
        self.format = pyaudio.paInt16
        self.channel_number = 1
        self.samp_rate = 44100
        self.chunk = 4096
        self.record_secs = record_secs   
        self.dev_index = 2
        self.wav_output_filename = 'record_{}.wav'
        self.record_counter = 0; 

    def record(self): 
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
                print("Recording for {} ...".format(self.record_secs))
        
        except Exception as e: 
            print(e)

        self._frames=[]
        _chunk_number = int((self.samp_rate/self.chunk)*self.record_secs)

        for ii in range(0,_chunk_number):
            data=self.stream.read(self.chunk, exception_on_overflow = False)
            self._frames.append(data)

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        
        if self.verbose: 
            print("finished recording")

        self._generate_wav_file()
        self.record_counter += 1

    def _generate_wav_file(self): 
        file_number = self.record_counter%5 
        wavefile=wave.open(wav_output_filename.format(file_number),'wb')
        wavefile.setnchannels(self.channel_number)
        wavefile.setsampwidth(self.audio.get_sample_size(self.format))
        wavefile.setframerate(self.samp_rate)
        wavefile.writeframes(b''.join(self._frames))
        wavefile.close()

if __name__ == "__main__":
    microphone = microphone(verbose=1)
    microphone.record()
