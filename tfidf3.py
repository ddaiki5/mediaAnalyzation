import re
import os.path
import glob
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from collections import Counter
import numpy as np

tokenizer = MeCab.Tagger("-Ochasen")
tokenizer.parse("")
blockWords=[]
def extract(text):
    words = []
    node = tokenizer.parseToNode(text)
    f = 0
    c = []
    while node:
        # if node.surface ==">" or node.surface =="<"or node.surface =="＞" or node.surface =="＜":
        #     f=1
        #     break
        if node.feature.split(",")[0] == u"名詞":
            if node.feature.split(",")[1] == u"一般" or node.feature.split(',')[1]==u"固有名詞":
                if re.match(r"[a-zA-Z]+", node.surface) or len(node.surface)>10:
                    pass
                else:
                    if node.surface not in blockWords:
                        words.append(node.surface)
        c.append(node.surface)
        node = node.next
    text = " ".join(c)
    text_result = " ".join(words)
    if f==1:
        text_result=""
    return text_result, text
bodyText = open("body26.txt", mode="rt", encoding="utf-8")
i=0
passNum = []
dic = []
keys = []
comment = []
sentences = []
sentenceVec = []
cs_arrays = []

def vecs_array(documents):
    do = np.array(documents)
    Vector = TfidfVectorizer(analyzer=split_words,binary=True,use_idf=False)
    vec = Vector.fit_transform(do)
    #print(vec.toarray())
    return vec.toarray()

def split_words(text):
    node = tokenizer.parseToNode(text)
    w = []
    while node:
        w.append(node.surface)
        node = node.next
    return w



for l in bodyText:
    i+=1
    if i>5000:break
    # if i<198000:continue
    # if i>200000:break
    docs = []
    sentences = l.split("/")
    
    text = l.replace("/", "")
    text = text.strip()
    text, co = extract(text)
    if text=="" or i==167230:
        passNum.append(i)
        continue
    docs.append(text)
    vectorizer = TfidfVectorizer(token_pattern=u'(?u)\\b\\w+\\b')
    x = vectorizer.fit_transform(docs)
    values = x.toarray()
    feature_names = vectorizer.get_feature_names()
    df = pd.DataFrame([feature_names,values.T], index=["1", "2"])
    df_0 = df[0:2].T
    df_0 = df_0.sort_values(by="2",ascending=False).reset_index(drop=True)
    print(i)
    print(len(sentences))
    s = df_0.iloc[:, 0].tolist()
    t = df_0.iloc[:, 1].tolist()
    d = dict(zip(s, t))
    #print(len(d))
    dic.append(d)
    keys.append(s)
    comment.append(co)
    #print(d)
    #print(s[0])
    #print(df_0.head(10))
    #print(df_0.head(2))
    sen = []
    # for s in sentences:
    #     sen.append(split_words(s))
    #     print(split_words(s))
    cs_array = cosine_similarity(vecs_array(sentences),vecs_array(sentences))
    print(len(cs_array))
    print(cs_array)
    cs_arrays.append(cs_array)
print(len(s))
print("-------------------")
bodyText.close()
bodyText = open("body26.txt", mode="rt", encoding="utf-8")
i=0
j=0
body = []
tfB = []
# for l in bodyText:
#   i+=1
#   if i in passNum:
#     continue
#   node = tokenizer.parseToNode(l)
#   keywords = []
#   l.
blockWord = ["<", ">", "誤字"]
flag = 0
passN = []
k=0
values = []
for l in bodyText:
  i+=1
  if i>5000:break
  #if i==1:continue
  # if i>200000:break
  # if i in passNum:
  #   continue
  l = l.strip()
  lines = l.split("/")
  keywords = []
  liness = []
  values = []
  j+=1
  print("-----------------")
  print(j-1, keys[j-1])
  for line in lines:
    t = []
    counter = 0
    value = 0
    node = tokenizer.parseToNode(line)
    while node:
      if node.feature.split(",")[0] == u"名詞":
        if node.feature.split(",")[1] == u"一般" or node.feature.split(',')[1]==u"固有名詞":
          if node.surface in keys[j-1]:
            value+=dic[j-1][node.surface]
            counter+=1
        #   if node.surface in blockWord:
        #     flag = 1
        #     break
      t.append(node.surface)
      node = node.next
    liness.append(t)
    values.append(value)
    keywords.append(counter)
  #j=0
  l=0
  m=0
  n=0
  o=0
  k+=1
  print(max(keywords))
  #print("a")
  #print(sorted(keywords))
#   if flag!=0:
#     passN.append(k)
#     continue
  if max(keywords)==0:
    passN.append(k)
    continue
  vId = list(zip(*reversed(sorted([(x, i) for i, x in enumerate(values)]))))[1]
  #print(len(values), len(vId), len(liness))
  print(vId)
  for c in keywords:
    if(c==max(keywords)):break
    n+=1
  l = -1.0
  n=0
#   print(vId)
#   print(cs_arrays[i-1])
#   print([len(v) for v in cs_arrays[i-1]])
#   print(vId[0])
#   print(len(cs_arrays[i-1]))
#   print(len(liness))
  
#   if vId[0]>=len(liness):
#       continue
#   if vId[0]>=len(cs_arrays[i]):
#       continue
  print("cs")
  print(cs_arrays[i-1][vId[0]])
  for c in cs_arrays[i-1][vId[0]]:
    if c>l and c<0.9999:
        l=c
        m=n
    n+=1
  l= -1.0
  n=0
  for c in cs_arrays[i-1][vId[0]]:
    if c>l and c<0.9999 and n!=m:
        l = c
        o = n
    n+=1
  print(keywords)
  print(len(cs_arrays[i-1]))
  print(m, o)
  if m==o:
      print("continue")
      continue
  
  #liness[vId[0]].append("[SEN]")
  liness[vId[0]].extend(liness[m])
  #liness[vId[0]].append("[SEN]")
  liness[vId[0]].extend(liness[o])
#   liness[m].append("[SEN]")
#   liness[m].extend(liness[l])
#   liness[m].append("[SEN]")
#   liness[m].extend(liness[n])
  text = "".join(liness[vId[0]])
  body.append(text)
  print(text)
  #if len(body)%20==0:print(str(i)+" "+text)

# i=0
# n=0
# co = []
# for l in comment:
#   i+=1

#   if i in passN:continue
#   co.append(l)
#   n+=1
# print(n)

# with open("comment_test.txt", mode="w", encoding='utf-8') as f:
#     f.write('\n'.join(co))
with open("test26.txt", mode="w", encoding='utf-8') as f:
    f.write('\n'.join(body))



