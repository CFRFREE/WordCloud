# @formatter:on


from wordcloud import WordCloud
from traceback import format_exc
from math import log
import time
import re

# 以下为全局变量，分别为字典形式的前缀词trie树、没实际意义而要去除的停顿词、总词汇频数及其对数
predict = {}
stopwords = []
tot = 0
logtot = 0


# 求前缀trie树
def GetDict():
	# 声明是全局变量
	global predict
	global tot
	global logtot
	with open("resources/dict.txt", 'r', encoding='utf-8') as f:
		content = f.read()
	f.close()
	# 读入resources/dict.txt中的文本信息，即常用词及其频数
	alist = content.split('\n')
	for item in alist:
		# word为词语本身，freq为其频数
		word, freq = item.split()[:2]
		freq = int(freq)
		tot += freq
		predict[word] = freq
		st = ""
		# 将每个词语的所有前缀都存入trie
		for ch in word:
			st += ch
			if st not in predict:
				predict[st] = 0
	# 求总频数的对数
	logtot = log(tot)


# 获取无意义的停顿词
def GetStopWords():
	global stopwords
	with open('resources/stop_words.txt', 'r', encoding='utf-8') as f:
		stopwords = f.read().split()
	f.close()


# 分词算法的主要部分
def work(sentence):
	DAG = {}
	n = len(sentence)
	tar = list(range(n))
	ans = []

	# 构建当前句子的有向无环图
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
			# 在DAG[pos]里存放pos位置开始的所有结束位置
			DAG[pos] = teplist
		return DAG

	# 使用动态规划求最大概率路径
	def DP():
		# 初始每个位置dp值为0
		dp = [0] * (n + 1)
		global logtot
		dp[n] = 0
		# 从后往前进行状态转移
		for i in range(n - 1, -1, -1):
			flag = 0
			for x in DAG[i]:
				# 如果当前转移的概率大于dp[i]就转移，寻找最大值
				if flag == 0 or log(predict[sentence[i:x + 1]] or 1) - logtot + dp[x + 1] > dp[i]:
					dp[i] = log(predict[sentence[i:x + 1]] or 1) - logtot + dp[x + 1]
					# tar存放从哪里转移来的
					tar[i] = x
					flag = 1

	# 根据tar数组记录的位置进行词的划分，返回一个list
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
	# 在一次使用中，前缀trie树和停顿词可以提前预处理以减少时空开支
	# 分词前使用正则对文本进行清洗和划分
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
		# 切割词语
		wordlist = cut(st)
		# 使用空格链接词语
		space_list = ' '.join(wordlist)
		# print(space_list)
		# 生成云图
		wordcloud = WordCloud(font_path='msyh.ttc', width=L, height=W, background_color="white", margin=1,
		                      max_words=300, min_font_size=20, max_font_size=None, repeat=True, mode='RGBA',
		                      colormap='tab10').generate(space_list)
		FileName = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
		wordcloud.to_file('output/' + FileName + '.png')
		return [1, FileName]
	except:
		# 如果生成失败就返回错误信息
		return [0, format_exc()]
