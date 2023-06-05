# import nltk
# #nltk.download('stopwords')
# from nltk.corpus import stopwords
# from nltk.cluster.util import cosine_distance
# import numpy as np
# import networkx as nx
import spacy
import json
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

stopwords = list(STOP_WORDS)


def read_content(file_name):
    file = open(file_name,"r",encoding= 'unicode_escape')
    filedata = file.readlines()
    article = filedata[0].split(". ")
    print(article,"hi and hello")
    sentences = []
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()
    listToStr = ' '.join([str(elem) for elem in sentences])
    return listToStr

punctuation = punctuation + '\n'

def generate_summary(file_name):
    print(file_name)
    content = read_content(file_name)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(content)
    tokens = [token.text for token in doc]
    print("hello",tokens)
    
    #punctuation
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())
    print(max_frequency)
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency
    
    sentence_tokens = [sent for sent in doc.sents]
    print(sentence_tokens)
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    print(sentence_scores)
    #select_length = int(len(sentence_tokens)*0.3)
    #print(select_length)
    summary = nlargest(10,sentence_scores, sentence_scores.get)
    print(summary)
    final_summary = [word.text for word in summary]
    print(final_summary)
    #listToStr = ' '.join([str(elem) for elem in sentences])
    #return listToStr
    #summary = " ".join([str(i) for i in final_summary])
    print("hello there",summary)
    #string = ' '.join([str(i) for i in final_summary])
    #string = json.dumps(final_summary)
    #print("hi?>?>?>", string)
    summary = ' '.join(final_summary)
    return summary

# def sentence_similarity(sent1, sent2, stopwords=None):
#     if stopwords is None:
#         stopwords = []
#     sent1 = [w.lower() for w in sent1]
#     sent2 = [w.lower() for w in sent2]
#     all_words = list(set(sent1+sent2))

#     vector1 = [0] * len(all_words)
#     vector2 = [0] * len(all_words)
#     for w in sent1:
#         if w in stopwords:
#             continue
#         vector1[all_words.index(w)] += 1
#     for w in sent2:
#         if w in stopwords:
#             continue
#         vector2[all_words.index(w)] += 1
#     return 1-cosine_distance(vector1, vector2)

# def generate_similarity_matrix(sentences, stop_words):
#     similarity_matrix = np.zeros((len(sentences),len(sentences)))
#     for idx1 in range(len(sentences)):
#         for idx2 in range(len(sentences)):
#             if idx1 == idx2:
#                 continue
#             similarity_matrix[idx1, idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

#     return similarity_matrix

# def generate_summary(file_name, top_n=5):
#     stop_words = stopwords.words('english') 
#     summarize_text = []
#     sentences = read_content(file_name)
#     sentences_similarity_matrix = generate_similarity_matrix(sentences,stop_words)
#     sentences_similarity_graph = nx.from_numpy_array(sentences_similarity_matrix)
#     scores = nx.pagerank(sentences_similarity_graph)
#     ranked_sentences = sorted(((scores[i],s)for i,s in enumerate(sentences)),reverse = True)
#     for i in range(top_n):
#         summarize_text.append(" ".join(ranked_sentences[i][1]))
#     return summarize_text 




