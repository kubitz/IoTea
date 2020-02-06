from textblob import TextBlob
emotion = TextBlob("I killed my son. I had a great day today. I love my wife but I shot her to death.")

for sentence in emotion.sentences:
    print(sentence, sentence.sentiment.polarity)