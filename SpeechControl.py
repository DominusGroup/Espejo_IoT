#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()

# setting threshold
r.energy_threshold = 300
r.dynamic_energy_threshold = False

with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source, timeout = 4)

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    audio2text = r.recognize_google(audio, key = None, language = "es-ES", show_all = False)
    print("Google Speech Recognition thinks you said: " + audio2text)
    ##b = audio.get_raw_data(convert_rate = None, convert_width = None)
    
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

