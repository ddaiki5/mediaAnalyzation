# coding: UTF-8
import os
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
from gensim.models import word2vec
import csv
import pickle

samples = [[0, 0, 0], [255, 255, 255], [255, 0, 0], [255, 127, 0], [255, 255, 0],\
           [127, 255, 0], [0, 255, 0], [0, 255, 127], [0, 255, 255], [0, 127, 255],\
           [0, 0, 255], [127, 0, 255], [255, 0, 255], [255, 0, 127]]
l = []
word_list = []

#結果から各色彩の生起確率を求める

with open('result.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fl = [int(v)/12 for v in row[1:]]
        word_list.append(row[0])
        l.append(fl)


def print_most_similar(word, n=5):
    print(word)
    words = model.wv.most_similar(positive=[word], topn=n)
    for i, w in enumerate(words, 1):
        print(str(i) + "    " + w[0] + "    " + str(w[1]))

model = word2vec.Word2Vec.load('./word2vec.model')

target = ["アタフタ", "あつあつ", "いがいが", "いじいじ", "イライラ", "ウキー", "ウキウキ", "うじゃうじゃ", "うとうと", "うろうろ", "うえーん", "えーん", "オギャーオギャー", "おどおど", "カーカー", "グワッグワッ", "ガーガー", "ガオー", "パシャ", "カシャ", "カタカタ", "ガタガタ", "ガツガツ", "がっかり", "ガヤガヤ", "カラカラ", "ガラガラ", "カリカリ", "ガリガリ", "カンカン", "ガンガン", "キーキー", "ギコギコ", "ギザギザ", "ギスギス", "キツキツ", "ぎっしり", "ぎとぎと", "ギュウギュウ", "きょろきょろ", "ぎょろぎょろ", "キラキラ", "キリキリ", "ギリギリ", "キンキン", "キンコンカンコン", "ぐいぐい", "グウグウ", "グキッ", "くすくす", "くちゃくちゃ", "グツグツ", "ぐっすり", "くどくど", "くねくね", "グビグビ", "クラクラ", "グラグラ", "くるくる", "ぐるぐる", "クンクン", "グングン"]
for tar in target:
    a = [0]*14
    if tar in word_list:
        continue
    if tar in model.wv:
        word_list.append(tar)
        for i in range(10):
            s = model.wv.similarity(tar, word_list[i])
            if s>0.2:
                for j in range(14):
                    a[j] += s*l[i][j]
        l.append(a)
print(len(l))

def color_vector(tar):
    a = [0]*14
    word_list.append(tar)
    for i in range(62):
        s = model.wv.similarity(tar, word_list[i])
        if s>0.2:
            for j in range(14):
                a[j] += s*l[i][j]
    return a


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_vector(text):
    char_filters = [UnicodeNormalizeCharFilter(), #Unicodeを正規化することで表記ゆれを吸収
                    RegexReplaceCharFilter('<.*?/\。、>', '')] #正規表現パターンにマッチした文字列を置換
    token_filters = [POSStopFilter(["名詞,数", "助詞","助動詞"]),
                     LowerCaseFilter(), #英字を小文字にする
                     ExtractAttributeFilter('surface')] # トークンから抽出する属性
    tokenizer = Tokenizer("Onomatope.csv", udic_enc="SHIFT-JIS")
    #print("o")
    analyzer = Analyzer(char_filters = char_filters, tokenizer = tokenizer, token_filters=token_filters)
    #print("ok")
    words = []
    c = ''
    i =0
    for s in text.split("\n"):
        i+=1
        if s[:5] == c:
            continue
        if i>1000:
            break
        c = s[:5]
        sen = []
        tokens = analyzer.analyze(s)
        #print(tokens)
        #print("okk")
        #print(tokens)
        sum = [0]*100
        j = 0
        for word in tokens:  
            #print(word) 
            if word in model.wv:
                key = color_vector(word) 
                for k in range(14):
                    sum[k] += key[k]
                j+=1
        #print(words)
        for k in range(14):
            sum[k] = sum[k]/j
        words.append(sum)
    return words

import numpy as np

def cos_sim(v1, v2):
    return np.dot(np.array(v1), np.array(v2)) / (np.linalg.norm(np.array(v1)) * np.linalg.norm(np.array(v2)))

sentences = []
# for f_path in ["body26","test26"]:
#     text = read_file(f_path+".txt")
#     print(text[:200])
#     w = get_vector(text)
#     f = open(f_path+"vd.pkl", 'wb')
#     pickle.dump(w, f)
#     sentences.append(w)
with open('body26vd.pkl', 'rb') as f:
        l = pickle.load(f)
sentences.append(l)
with open('test26vd.pkl', 'rb') as f:
    l = pickle.load(f)
sentences.append(l)
print(len(sentences[0]))
s = 0
v = 0
for i in range(200):
    s += cos_sim(sentences[0][i], sentences[1][i])
    v += cos_sim(sentences[0][i], sentences[1][i])*cos_sim(sentences[0][i], sentences[1][i])
    print(cos_sim(sentences[0][i], sentences[1][i]))
print(s/200, v/200)




