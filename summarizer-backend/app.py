"""
Project Name: Summarizer
YouTube Transcript Summarizer API
"""

#from crypt import methods
from importlib.resources import path
import os
# import sumy
from flask import Flask, request, jsonify, flash, request, redirect, url_for, session
from flask_session.__init__ import Session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import speech_recognition as sr
from pydub import AudioSegment 

# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.lsa import LsaSummarizer

from bs4 import BeautifulSoup
import requests

import nltk
import pandas as pd

from model import nlp_model
import fileSummary
import videoSummary

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)
sess = Session()


@app.route('/api/', methods=['GET'])
def respond():

    # Retrieve the video_id from url parameter
    vid_url = request.args.get("video_url", None)

    if "youtube.com" in vid_url:

        try:
            video_id = vid_url.split("=")[1]

            try:
                video_id = video_id.split("&")[0]

            except:
                video_id = "False"

        except:
            video_id = "False"

    elif "youtu.be" in vid_url:

        try:
            video_id = vid_url.split("/")[3]

        except:

            video_id = "False"

    else:
        video_id = "False"

    # For debugging
    # print(f"got name {video_id}")

    body = {}
    data = {}

    # Check if user doesn't provided  at all
    if not video_id:
        data['message'] = "Failed"
        data['error'] = "no video id found, please provide valid video id."

    # Check if the user entered a invalid instead video_id
    elif str(video_id) == "False":
        data['message'] = "Failed"
        data['error'] = "video id invalid, please provide valid video id."

    # Now the user has given a valid video id
    else:

        if nlp_model(video_id) == "0":
            data['message'] = "Failed"
            data['error'] = "API's not able to retrive Video Transcript."

        else:
            data['message'] = "Success"
            data['id'] = video_id
            data['original_txt_length'], data['final_summ_length'], data['eng_summary'], data['hind_summary'], data['guj_summary'] = nlp_model(
                video_id)

    body["data"] = data

    # Return the response in json format
    return buildResponse(body)


# Welcome message to our server
@app.route('/')
def index():

    body = {}
    body['message'] = "Success"
    body['data'] = "Welcome to YTS API."

    return buildResponse(body)


def buildResponse(body):

    # from flask import json, Response
    # res = Response(response=json.dumps(body), status=statusCode, mimetype="application/json")
    # res.headers["Content-Type"] = "application/json; charset=utf-8"
    # return res

    response = jsonify(body)
    # response.headers.add('Access-Control-Allow-Origin', '*')

    return response


# for websites.......

@app.route("/api/website/", methods=["GET"])
def web_sum():
    print("hello")
    web_url = request.args.get("web_url", None)
    url_content = top10_sent(web_url)
    return url_content


def get_wiki_content(url):
    print("hello")
    req_obj = requests.get(url)
    text = req_obj.text
    soup = BeautifulSoup(text,'html.parser')
    all_paras = soup.find_all("p")
    wiki_text = ''
    for para in all_paras:
        wiki_text += para.text
    return wiki_text


def top10_sent(url):
    body = {}
    data = {}
    print("hello")
    required_text = get_wiki_content(url)
    stopwords = nltk.corpus.stopwords.words("english")
    sentences = nltk.sent_tokenize(required_text)
    words = nltk.word_tokenize(required_text)
    word_frequency = {}
    for word in words:
        if word not in stopwords:
            if word not in word_frequency:
                word_frequency[word] = 1
            else:
                word_frequency[word] += 1

    max_word_freq = max(word_frequency.values())
    for key in word_frequency.keys():
        word_frequency[key] /= max_word_freq


    sentences_score = []
    for sent in sentences:
        curr_words = nltk.word_tokenize(sent)
        curr_score = 0
        for word in curr_words:
            if word in word_frequency:
                curr_score += word_frequency[word]
        sentences_score.append(curr_score)
    

    sentences_data = pd.DataFrame({"sent": sentences, "score": sentences_score})
    sorted_data = sentences_data.sort_values(by= "score",ascending=False).reset_index()
    top10_rows = sorted_data.iloc[0:11,:]
    #top10 = list(sentences_data.sort_values(by= "score",ascending=False).reset_index().iloc[0:11,"sentences"])
    #body = {}
    data['message'] = "Success"
    data['original_txt_length'] = "" 
    data['final_summ_length'] = ""
    data['eng_summary'] = list(top10_rows["sent"])
    #new_data = dict.fromkeys(data, "data")
    #print(list(top10_rows["sent"]))
    body['data'] = data
    print(buildResponse(body))
    return buildResponse(body)




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/uploadfile", methods=["GET", "POST"])
def file_summary():
    print("file hello")
    data = {}
    body = {}
    if request.method == 'POST':
        f = request.files['myFile']
        f.save(secure_filename(f.filename))
    file = open(f.filename,"r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    #print(article)
    textContent = fileSummary.generate_summary(f.filename)
    print(textContent)
    data['message'] = "Success"
    data['original_txt_length'] = "none"
    data['final_summ_length'] = len(textContent)
    data['eng_summary'] = textContent
    #new_data = dict.fromkeys(data, "data")
    #print(list(top10_rows["sent"]))
    body['data'] = data
    print(body['data'])
    print(buildResponse(body))
    return buildResponse(body)
      
    #return 'file uploaded successfully'


@app.route("/api/video", methods=["GET", "POST"])
def video_summary():
    print("file hello")
    data = {}
    body = {}
    if request.method == 'POST':
        print(request.files['myFile'])
        f = request.files['myFile']
        f.save(secure_filename(f.filename))
    file = open(f.filename)
    textContent = videoSummary.generateVideoSummary(f.filename)
    print(textContent)
    data['message'] = "Success"
    data['original_txt_length'] = "none"
    data['final_summ_length'] = len(textContent)
    data['eng_summary'] = textContent
    body['data'] = data
    print(body['data'])
    print(buildResponse(body))
    return buildResponse(body)


if __name__ == '__main__':

    # Threaded option to enable multiple instances for multiple user access support
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    #app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    sess.init_app(app)

    app.debug = True
    app.run()

# Deployment to Heroku Cloud.
