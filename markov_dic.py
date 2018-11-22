#!/usr/bin/env python
# coding: utf-8

# In[12]:


from janome.tokenizer import Tokenizer
import re
import random

markov={}
sentence = ""

def parse(text):
	"""形態素解析によって形態素を取り出す
		text : マルコフ辞書のもととなるテキスト
		戻り値 : 形態素のリスト
	"""
	t = Tokenizer()
	tokens = t.tokenize(text)
	result=[]
	for token in tokens:
		result.append(token.surface)
	return(result)

def get_morpheme(filename):
	"""ファイルを読み込み、形態素のリストをつくる
		filename : マルコフ辞書のもとになるテキストファイル
		戻り値 : 形態素リスト
	"""
	with open(filename,"r",encoding="utf-8") as f:
		text = f.read()
	text = re.sub("\n","",text) # 文末の改行文字を取り除く
	wordlist = parse(text)
	return wordlist

def create_markov(wordlist):
	"""マルコフ辞書を作成する
		wordlist : 全テキストから抽出した形態素リスト
	"""
	p1=""
	p2=""
	p3=""

	for word in wordlist:
		# p1,p2,p3のすべての値が格納されるか
		if p1 and p2 and p3:
			# markovに(p1,p2,p3)キーが存在するか
			if(p1,p2,p3) not in markov:
				# なければキー:値のペアを追加
				markov[(p1,p2,p3)] = []
			# キーのリストにサフィックス追加
			markov[(p1,p2,p3)].append(word)
		# 3つのプレフィックスの値を置き換える
		p1,p2,p3=p2,p3,word

def generate(wordlist):
	"""マルコフ辞書から文章を取り出してsentenceを格納する
		wordlist : 全テキストから抽出した形態素リスト
	"""

	global sentence
	# markovのキーをランダムに抽出し、プレフィックスに1-3に代入
	p1,p2,p3 = random.choice(list(markov.keys()))
	count=0
	while count < len(wordlist):
		if((p1,p2,p3) in markov) == True : # キーが存在するかチェック
			tmp = random.choice(
				markov[(p1,p2,p3)]
			)
			sentence += tmp
		p1,p2,p3 = p2,p3,tmp
		count+=1
	sentence = re.sub('^.+?。','',sentence) #最初に出てくる句点までを除去

	if re.search('.+。',sentence): #最後の句点から先を取り除く
		sentence = re.search(".+。",sentence).group()
	
	sentence = re.sub('」','',sentence) # 閉じカッコを削除
	sentence = re.sub('「','',sentence) # 開きカッコを削除
	sentence = re.sub('　','',sentence) # 全角スペースを削除


def overlap():
	"""sentenceの重複した文章を取り除く
	"""
	global sentence
	sentence = sentence.split('。')# 。で分割リストを作る
	if '' in sentence:
		sentence.remove('')
	new = []
	for str in sentence:
		str = str+"。"
		if str =="。":
			break
		new.append(str)

	new = set(new)
	sentence = ''.join(new)

#
# 文章の出力
#
if __name__ == "__main__":
	word_list = get_morpheme("text.txt")
	create_markov(word_list)
	while(not sentence):
		generate(word_list)
		overlap()
	
	print (sentence)

