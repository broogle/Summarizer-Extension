import speech_recognition as sr
from pydub import AudioSegment
import os
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser 


def listToString(s): 
    
    str1 = " " 
    
    # return string  
    return (str1.join(s))


def generateVideoSummary(filename):
    print(filename, "Hiiii")
    #path = os.getcwd()
    AudioSegment.from_file(os.path.abspath(filename)).export("output.mp3", format="mp3")
    sound = AudioSegment.from_mp3("output.mp3")
    audio_file = "trans.wav"
    sound.export(audio_file, format="wav")
    # file_path = "trans.wav"
    # data, samplerate = soundfile.read(file_path)
    # soundfile.write(file_path, data, samplerate)
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    
    text = r.recognize_google(audio)
    print(text)
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    lsa_summarizer = LsaSummarizer()
    lsa_summary = lsa_summarizer(parser.document,15)
    sentences = []
    for sentence in lsa_summary: 
        sentences.append(sentence)
    output = ' '.join([str(elem) for elem in sentences])
    print(output, "---------------------------------===")
    return output


# def generateVideoSummary(filename):
#     print(filename, 'hello and hiiii')
#     name = os.path.abspath(filename)
#     command = 'ffmpeg -i  -ab 160k -ar 44100 -vn audio.wav'
#     subprocess.call(command, shell=True) 