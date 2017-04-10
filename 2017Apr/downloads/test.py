#!/usr/bin/env python

"""
hw2_1.py
authour：	oyh
version:	hw2_1_v2
Date:		2017-03-15 21:47
Description: Homework Ch2 of Data Mining
			 数据平滑_数据分箱(等深分箱，均值法）
			 数据规范化: 最大最小值法
						 Z-score 规范化
						 小数定标规范化
分析答案(output)：

[13, 15, 16] --> 14.67
[16, 19, 20] --> 18.33
[20, 21, 22] --> 21.00
[22, 25, 25] --> 24.00
[25, 25, 30] --> 26.67
[33, 33, 33] --> 33.00
[35, 35, 35] --> 35.00
[35, 36, 40] --> 37.00
[45, 46, 52] --> 47.67
[70] --> 70.00

1）分箱平滑:
[14.67, 14.67, 14.67, 18.33, 18.33, 18.33, 21.0, 21.0, 21.0, 
24.0, 24.0, 24.0, 26.67, 26.67, 26.67, 33.0, 33.0, 33.0, 35.0, 35.0, 35.0, 
37.0, 37.0, 37.0, 47.67, 47.67, 47.67, 70.0]

			
"""

from functools import reduce
import numpy as np

age = [13,15,16,16,19,20,20,21,22,22,25,25,25,25,
		30,33,33,33,35,35,35,35,36,40,45,46,52,70]

def box_method(data, depth = 3, *, file = None):
	"""
	box_method(data, depth = 3, file = None) --> list object
	
	Slicing the given data with a customized depth(default value is 3)
	then replace all age's value in every sliced boxes with their avg
	return a list type data
	
	（1）此方法为同一权重法（等深分箱），适合分箱后箱内数据较为集中，受离异值
	影响较小；但对于分布不均匀的数据会加剧数据的波动
	（2）常见的平滑方法还包括：
	分箱：使用等宽分箱，分箱后还可以使用边界值或中位数平滑
	聚类：将特征值相似的数据归集为一群
	回归：按照合适的函数将噪声值趋近正常
	"""
	res = []
	data = sorted(data)
	while data:
		box, data = data[:depth], data[depth:]	#以给定深度分箱
		box_avg = round(reduce(lambda x, y: x+y, box)/len(box), 2)#求均值
		box_smooth = [box_avg] * len(box)
		if  file:
			#显示处理前后对比
			print('{} --> {:.2f}'.format(str(box), box_avg), file = file)
		else :
			print('{} --> {:.2f}'.format(str(box), box_avg), )
		res.extend(box_smooth)
	return(res)

def min_max(data, value = None):

	"""
	min_max(data, value = None) --> list Object
	
	min-max normalization find the maximal value and minimum value of the
	given data, thus calculate the range, using it as denominator;
	and normalie every item in the given data by dividing range
	"""
	
	max_value = max(data)
	min_value = min(data)
	Dom = max_value - min_value
	res = [(x-min_value)/Dom for x in data]
	if value == None:
		return res
	else:
		return res, value/Dom

def z_score(data, value = None):

	"""
	z_score(data, value = None) --> list Object
	
	Z-score method using numpy packet to caclulate mean and standard deviation
	of the given data, iter i in the list minus mean then
	divide the standard deviation
	"""
	
	std = np.std(data, ddof =1)
	mean = np.mean(data)
	res = [(x-mean)/std for x in data]
	if value == None:
		return res
	else:
		return res, (value-mean)/std
		
def decimal_scaling(data, value = None):

	"""
	decimal_scaling(data, value = None) --> list Object
	

	"""
	
	data_abs = map(abs, data)
	max_value = max(data_abs)
	j = 0
	while (max_value/pow(10, j)) > 1:
		j += 1
	base = pow(10, j)
	res = [x/base for x in data]
	if value == None:
		return res
	else:
		return res, value/base
	

if __name__ ==  '__main__':
	f = open('output.txt', 'w')
	print('分箱平滑:\n{}\n\n\
		最小-最大规范化 35 --> {:.2f}\n\
		Z-score规范化   35 --> {:.2f}\n\
		小数定标规范化  35 --> {:.2f}\n'.format(
		box_method(age, file=f), min_max(age, 35)[1], 
		z_score(age, 35)[1],   decimal_scaling(age, 35)[1]),
		file = f)
	f.close()
	
