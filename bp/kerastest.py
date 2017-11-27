# coding:utf-8

import pandas as pd

from keras.models import Sequential
from keras.layers.core import Dense, Activation


# inputfile = 'input.xlsx'   #excel输入
# data = pd.read_excel(inputfile,index='Date',sheetname=0) #pandas以DataFrame的格式读入excel表
# data_train = data.loc[range(0,6)].copy() #标明excel表从第0行到520行是训练集
#
# print data


# # 构建模型
# model = Sequential()
# model.add(Dense(units=64, input_dim=100))
# model.add(Activation("relu"))
# model.add(Dense(units=10))
# model.add(Activation("softmax"))
#
# # 编译模型   loss损失函数和 optimizer优化器
# model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

# # 开始训练
# model.fit(x_train, y_train, epochs=5, batch_size=32)
#
#
# # 模型评估
# loss_and_metrics = model.evaluate(x_test, y_test, batch_size=128)
#
#
# # 模型预测
# classes = model.predict(x_test, batch_size=128)



