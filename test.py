#encoding=utf-8
import jieba.posseg as pseg
words = pseg.cut("例如我输入一个带“韩玉赏鉴”的标题，在自定义词库中也增加了此词为N类型")
for w in words:
 print w.word, w.flag