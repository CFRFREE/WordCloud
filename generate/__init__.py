from wordcloud import WordCloud
from jieba import cut
from traceback import format_exc


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
