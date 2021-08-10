# mediaAnalyzation

* color_analy.py
    * 結果から各色彩の生起確率を求めて、本を読む頻度による違いの平均と分散を求める
* crawler.py
    * 小説家になろうから本文と感想のペアをスクレイピングする
* tfidf3.py
    * tf-idfとコサイン類似度を使い、本文から生成に使う3文を選ぶ
* train_word2vec.py
    * janomeによる形態素解析とgensimによるword2vecのモデル学習を行う
* word_analysis.py
    * janome練習用
* word2color.py
    * 学習したモデルと結果から色彩ベクトルへの変換を行う
* word2vec.model
    * 学習したモデル
* body26wd.pkl、comment26wd.pkl
    * 前処理済形態素リスト
* body26vd.pkl、test26vd.pkl
    * 色彩ベクトルリスト
* Onomatope.scv
    * janomeユーザ辞書用　オノマトペ追加