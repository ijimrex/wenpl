#coding:utf-8

import thulac

thu1 = thulac.thulac(seg_only=True)  #设置模式为行分词模式
a = thu1.cut("我们全面优化了语义分析算法能客服机器人就在这里...",text=True)

print(a)
