# big_data_project01

##動作環境
Python3があればいけるよ、あ、、、、、、MeCabも必要

##ファイル
reader.py: データセットからデータを読み込むモジュール(MecabとMecab-Python3をinstall必須)

##メソッド
reader.py:  
1. create_list(filename):  
   第一引数に処理したいファイル。  
   ツイッターID、日付、リツイートタグ、リプ先、ツイート内容をクラス変数に保存してくれる。  
2. word_counter()  
   create_list()で作成されたリストself.textsをもとに各文字列を形態素解析にかけて品詞の頻度表を作成
   現段階では名詞だけしか頻度表はない（たぶん他は必要ない）
　　
