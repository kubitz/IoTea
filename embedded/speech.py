import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


class SpeechToText(): 
    def __init__(self): 
        self.client = speech.SpeechClient()
        self.file_name = os.path.join(os.path.dirname(__file__),'record_{}.wav')
        self.config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code='en-US', 
            enable_automatic_punctuation=True)

    def get_text(self, file_number): 
        with io.open(self.file_name.format(file_number), 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)
            response = self.client.recognize(self.config, audio)
            texts = self._format_response(response)
            return texts
    
    def _format_response(self, response): 
        texts = []
        for result in response.results: 
            texts.append(result.alternatives[0].transcript)
        
        return texts

if __name__ == "__main__":
    speech_to_text = SpeechToText()
    text = speech_to_text.get_text(0)
    print(text)