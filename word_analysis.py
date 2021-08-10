
#import MeCab
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import collections
t = Tokenizer("Onomatope.csv", udic_enc="SHIFT-JIS")
a = Analyzer(token_filters=[POSKeepFilter(['オノマトペ']), TokenCountFilter()])
#t = Tokenizer()
for token in t.tokenize('あっさりとしたスープが食べたい'):
    print(token)
# tokenizer = MeCab.Tagger("mecabrc -d /Users/daiki/ipadic -u /Users/daiki/onomatope.dic")
# tokenizer.parse("")

# def tokenize(sentence):
#     tag = tokenizer.parseToNode(sentence)
#     while tag:
#         features = tag.feature.split(',')
#         token = tag.surface
#         print(token, features)
#         tag = tag.next

        
# sample = u"あっさりアタフタあつあついじいじうきーうろうろえーん"
# #sample = sample.encode('EUC-JP')
# print(sample, type(sample))
# sample = tokenizer.parse(sample)
# print(sample)
# #tokenize(sample)

# ono = ["アタフタ","あつあつ","あっさり","いがいが","いじいじ","いちゃいちゃ","ウキー","ウキウキ","うじゃうじゃ","うっかり","うとうと","うるうる","うろうろ","うえーん","えーん","オギャーオギャー","おどおど","カーカー","グワッグワッ","ガーガー","ガオー","パシャ","カシャ","カタカタ","ガタガタ","ガツガツ","がっかり","ガヤガヤ","カラカラ","ガラガラ","カリカリ","ガリガリ","カンカン","ガンガン","キーキー","ギコギコ","ギザギザ","ギスギス","キツキツ","ぎっしり","ぎとぎと","ギュウギュウ","きょろきょろ","ぎょろぎょろ","キラキラ","キリキリ","ギリギリ","キンキン","キンコンカンコン","ぐいぐい","グウグウ","グキッ","くすくす","くちゃくちゃ","ぐちゃぐちゃ","グツグツ","ぐっすり","ぐったり","くどくど","くねくね","グビグビ","クラクラ","グラグラ","くるくる","ぐるぐる","クンクン","グングン"]



# commentText = open("body26.txt", mode="rt", encoding="utf-8")
# # comment = []
# # passNum = []
# cou = [0]*100
# i=0
# num=0
# for l in commentText:
#   i+=1
#   #node = tokenizer.parseToNode(l)
#   keywords = []
#   c = []
#   while node:
#     if node.feature.split(",")[0] == u"オノマトペ":
#       keywords.append(node.surface)
#     node = node.next
#   j = 0
#   for o in ono:
#       cou[j] += l.count(o)
#       j+=1
#   num+=1
# print(num)
# for i in range(len(ono)):
#     print(ono[i], cou[i])

# c = collections.Counter(keywords)
# print(c.most_common())

#bodyText = open("body1.txt", mode="rt", encoding="utf-8")
#i=0
#body = []
# for l in bodyText:
#   i+=1
#   if i in passNum:
#     continue
#   node = tokenizer.parseToNode(l)
#   keywords = []
#   l.
# for l in bodyText:
#   i+=1
#   if i in passNum:
#     continue
#   node = tokenizer.parseToNode(l)
#   keywords = []
#   while node:
#     if node.feature.split(",")[0] == u"名詞":
#       if node.feature.split(",")[1] == u"一般" or node.feature.split(',')[1]==u"固有名詞":
#         if node.surface not in keywords:
#           keywords.append(node.surface)
#     node = node.next
#   #print(keywords)
#   keys = ' '.join(keywords)
#   print(keys)
#   body.append(keys)

