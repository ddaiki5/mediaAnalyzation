import os
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
from gensim.models import word2vec
import pickle

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def tokenizer(text):
    char_filters = [UnicodeNormalizeCharFilter(), #Unicodeを正規化することで表記ゆれを吸収
                    RegexReplaceCharFilter('<.*?/\。、>', '')] #正規表現パターンにマッチした文字列を置換
    token_filters = [POSStopFilter(["名詞,数"]),
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
        if i>20000:
            break
        c = s[:5]
        sen = []
        tokens = analyzer.analyze(s)
        #print(tokens)
        #print("okk")
        #print(tokens)
        for word in tokens:  
            #print(word)    
            sen.append(word)
        #print(words)
        words.append(sen)
        print(i, len(words))
    return words



if __name__ == '__main__':
    sentences = []
    # for f_path in ["comment26"]:
    #     text = read_file(f_path+".txt")
    #     print(text[:200])
    #     w = tokenizer(text)
    #     f = open(f_path+"wd.pkl", 'wb')
    #     pickle.dump(w, f)
    #     sentences.append(tokenizer(text))
    
    with open('body26wd.pkl', 'rb') as f:
        l = pickle.load(f)
    sentences = l
    with open('comment26wd.pkl', 'rb') as f:
        l = pickle.load(f)
    sentences.extend(l)
    model = word2vec.Word2Vec(sentences, vector_size=100, window=5,
                              min_count=3, workers=5, sg=0, hs=0,
                              negative=5, cbow_mean=1, sample=1e-3,
                              epochs=10)
    model.save('./word2vec.model')
    