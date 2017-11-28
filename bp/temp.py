# coding:utf-8

# 使用keras框架对订单和交易额预测


import numpy as np
import matplotlib.pyplot as plt

# 是否节假日
holiday = [0,0,0,2,2,0,0,0,0,0,2,1,1,1,1,0,0,0,0,0,2,2,0,0,0,0,0,2,2,0,0,0]
# 星期数
weeknum = [3,4,5,6,7,1,2,3,4,5,6,4,5,6,7,1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3]
# 补贴率
subsidyrate = [0.0409,0.0318,0.0315,0.0315,0.0256,0.0277,0.0294,0.0285,0.0349,0.0307,0.0322,0.0215,0.0271,0.031,0.028,0.0293,0.0345,0.0318,0.0296,0.0353,0.0286,0.0251,0.0328,0.0322,0.0294,0.0297,0.0306,0.0298,0.0319,0.0333,0.034,0.0387]
# 上线天数
onlinedays = [123,124,125,126,127,128,129,130,131,132,133,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158]
# 菜品数量
foodnum = [48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,50,50,50,50,50,50,50,50,50]

# 输出层
# 交易额
tradesum = [19934.51,17134.9,17538.9,15480.7,12775,14368.22,16588.11,13413.4,13220.21,14730.39,	13705.6,7758.4,10150.6,10076.7,9818.81,10411.1,13207.3,12060.6,13499.51,12766.7,10115.79,12723,12922.2,13991,13548.19,11188.4,13650.52,11011.6,	9719.4,	10796.2,11976.3,10596.19]
# 订单数
ordernum = [481,406,423,362,301,340,394,331,324,341,320,186,233,238,239,255,330,292,321,316,244,297,314,342,327,269,324,270,230,271,295,266]

# 输入值
samplein = np.mat([holiday,weeknum,subsidyrate,onlinedays,foodnum]) #5*32
sampleinminmax = np.array([samplein.min(axis=1).T.tolist()[0],samplein.max(axis=1).T.tolist()[0]]).transpose()#3*2，对应最大值最小值
# 输出值
sampleout = np.mat([tradesum,ordernum])#2*32
sampleoutminmax = np.array([sampleout.min(axis=1).T.tolist()[0],sampleout.max(axis=1).T.tolist()[0]]).transpose()#2*2，对应最大值最小值

#5*32
sampleinnorm = (2*(np.array(samplein.T)-sampleinminmax.transpose()[0])/(sampleinminmax.transpose()[1]-sampleinminmax.transpose()[0])-1).transpose()
#2*32
sampleoutnorm = (2*(np.array(sampleout.T).astype(float)-sampleoutminmax.transpose()[0])/(sampleoutminmax.transpose()[1]-sampleoutminmax.transpose()[0])-1).transpose()

from keras.models import Sequential
from keras.layers import Dense, Activation

model = Sequential()
model.add(Dense(7, input_dim=5, activation='tanh'))
model.add(Dense(2, activation='tanh'))

model.compile(optimizer='rmsprop', loss='mse')
model.fit(sampleinnorm.T, sampleoutnorm.T, epochs=100, batch_size=10)

fig, axes = plt.subplots(2, 1)
axes[0].plot(range(32), model.predict(sampleinnorm.T)[:,0])
axes[0].plot(range(32), sampleoutnorm.T[:,0])
axes[1].plot(range(32), model.predict(sampleinnorm.T)[:,1])
axes[1].plot(range(32), sampleoutnorm.T[:,1])



fig.savefig('result.png')
