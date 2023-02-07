# @formatter:on


from wordcloud import WordCloud
from traceback import format_exc
from math import log
import re

predict = {}
stopwords = []
tot = 0
logtot = 0


def GetDict():
	global predict
	global tot
	global logtot
	with open("resources/dict.txt", 'r', encoding='utf-8') as f:
		content = f.read()
	f.close()
	alist = content.split('\n')
	for item in alist:
		word, freq = item.split()[:2]
		freq = int(freq)
		tot += freq
		predict[word] = freq
		st = ""
		for ch in word:
			st += ch
			if st not in predict:
				predict[st] = 0
	logtot = log(tot)


def GetStopWords():
	global stopwords
	with open('resources/stop_words.txt', 'r', encoding='utf-8') as f:
		stopwords = f.read().split()
	f.close()


def work(sentence):
	DAG = {}
	n = len(sentence)
	tar = list(range(n))
	ans = []

	def GetDAG():
		for pos in range(n):
			teplist = []
			tepst = sentence[pos]
			R = pos
			while tepst in predict:
				if predict[tepst] > 0:
					teplist.append(R)
				R += 1
				if R >= n:
					break
				tepst += sentence[R]
			if len(teplist) == 0:
				teplist.append(pos)
			DAG[pos] = teplist
		return DAG

	def DP():
		dp = [0] * (n + 1)
		global logtot
		dp[n] = 0
		for i in range(n - 1, -1, -1):
			flag = 0
			for x in DAG[i]:
				if flag == 0 or log(predict[sentence[i:x + 1]] or 1) - logtot + dp[x + 1] > dp[i]:
					dp[i] = log(predict[sentence[i:x + 1]] or 1) - logtot + dp[x + 1]
					tar[i] = x
					flag = 1

	def CutSentence():
		pos = 0
		while pos < n:
			if sentence[pos:tar[pos] + 1] not in stopwords:
				ans.append(sentence[pos:tar[pos] + 1])
			pos = tar[pos] + 1

	GetDAG()
	DP()
	CutSentence()
	return ans


def cut(st):
	GetDict()
	GetStopWords()
	r = "[_.!+-=——,$%^，。？?、~@#￥%……&*《》<>「」{}【】()/A-Za-z]"
	st = re.sub(r, ' ', st)
	alist = st.split()
	ans = []
	for item in alist:
		try:
			ans.extend(work(item))
		except:
			print(item)
	return ans


def work_text(st, L, W):
	try:
		wordlist = cut(st)  # 切割词语
		space_list = ' '.join(wordlist)  # 空格链接词语
		# print(space_list)
		wordcloud = WordCloud(font_path='simsun.ttc', width=L, height=W, background_color="white", margin=1,
		                      max_words=300, min_font_size=20, max_font_size=None, repeat=True, mode='RGBA',
		                      colormap='tab10').generate(space_list)  # 生成云图
		wordcloud.to_file('output/wordcloud.png')
		return "生成成功"
	except:
		return format_exc()
