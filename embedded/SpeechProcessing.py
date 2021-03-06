import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from time import perf_counter 
from textblob import TextBlob
from TwitterBot import TwitterBot



credential_path = r"/home/pi/embedded_imperial/embedded/apikey.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

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
        """ Makes an API request to Google Cloud Speech-to-text 
            Input: file_number to load .wav file generated by RecordMic in the format "record_#.wav" where "#" is file number
            Output: List of texts. A text can be composed of several sentences. Each text correspond to a different speaker in the conversation recorded. 
        """

        with io.open(self.file_name.format(file_number), 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)
            response = self.client.recognize(self.config, audio)
            texts = self._format_response(response)
            return texts
    
    def _format_response(self, response): 
        """ Formats Google Speech-to-text API response. 
            Selects the most probable transcript for each text. Each text correspond to a different speaker in the recorded conversation. 
            Input: response object from API client
            Output: List of texts. 
        """
        texts = []
        for result in response.results: 
            texts.append(result.alternatives[0].transcript)
        return texts
    
    def get_sentiment(self, texts): 
        """ Get the sentiment from a text for each sentence. 
            The sentiment is represented by a value between [-1, 1]
            Input: a list of texts (each text can be a group of unparsed sentences)
            Output: List of tuples (sentence, sentiment) sorted by sentiment (lowest index corresponds to lowest sentiment)
        """
        list_sentiments = []

        for text in texts: 
            sentiments = TextBlob(text)
            for sentence in sentiments.sentences: 
                list_sentiments.append((str(sentence), sentence.sentiment.polarity))
        
        list_sentiments = self._sort_sentiments(list_sentiments)
        return list_sentiments
    
    def get_average_sentiment(self, list_sentiments): 
        """ Returns average sentiment from a whole conversation 
            The average sentiment is represented by a value between [-1, 1]
            Input: list of sentiments (returned by get_sentiment)
            Output: Value between [-1, 1]
        """
        average_polarity = 0
        for sentiment in list_sentiments: 
            polarity = sentiment[1]
            average_polarity += polarity 
        average_polarity /= len(list_sentiments)
        return average_polarity

    def _sort_sentiments(self, list_sentiments): 
        """Sort a list of tuples containing the sentence and its associated sentiment (value between [-1:1])
            Input: list of tuple (sentence, sentiment)
            Output: Sorted list of tuples
        """
        list_sentiments.sort(key = lambda x: x[1])  
        return list_sentiments  

    

if __name__ == "__main__":
    t1_start = perf_counter()  
    speech_to_text = SpeechToText()
    twitter_bot = TwitterBot()

    result = speech_to_text.get_text(0)
    sentiments = speech_to_text.get_sentiment(result)
    twitter_bot.send_tweet(sentiments[0][0])
    t1_stop = perf_counter() 
    print("Elapsed time during the whole program in seconds:", t1_stop-t1_start)
    print(sentiments)


