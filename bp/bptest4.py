# coding:utf-8

#1 数据输入
import xlrd
import pandas as pd
inputfile = 'input.xlsx'   #excel输入
outputfile = 'output.xls' #excel输出
modelfile = 'modelweight.model' #神经网络权重保存
data = pd.read_excel(inputfile,index='Date',sheetname=0) #pandas以DataFrame的格式读入excel表
feature = ['F1','F2','F3','F4'] #影响因素四个
label = ['L1'] #标签一个，即需要进行预测的值
data_train = data.loc[range(0,6)].copy() #标明excel表从第0行到520行是训练集

#2 数据预处理和标注
data_mean = data_train.mean()
data_std = data_train.std()
data_train = (data_train - data_mean)/data_std #数据标准化
x_train = data_train[feature].as_matrix() #特征数据
y_train = data_train[label].as_matrix() #标签数据

 #3 建立一个简单BP神经网络模型
from keras.models import Sequential
from keras.layers.core import Dense, Activation
model = Sequential()  #层次模型
model.add(Dense(12,input_dim=4,init='uniform')) #输入层，Dense表示BP层
model.add(Activation('relu'))  #添加激活函数
model.add(Dense(1,input_dim=12))  #输出层
model.compile(loss='mean_squared_error', optimizer='adma') #编译模型
model.fit(x_train, y_train, nb_epoch = 1000, batch_size = 6) #训练模型1000次
model.save_weights(modelfile) #保存模型权重

#4 预测，并还原结果。
x = ((data[feature] - data_mean[feature])/data_std[feature]).as_matrix()
data[u'L1_pred'] = model.predict(x) * data_std['L1'] + data_mean['L1']

#5 导出结果
data.to_excel(outputfile)

#6 画出预测结果图
import matplotlib.pyplot as plt
p = data[['L1','L1_pred']].plot(subplots = True, style=['b-o','r-*'])
plt.show()