# coding:utf-8


# bp神经网络算法对未来订单量、交易额的预测

import numpy as np
import matplotlib.pyplot as plt

def logsig(x):
    return 1/(1+np.exp(-x))

# 输入层
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
sampleout = np.mat([ordernum,tradesum])#2*32
sampleoutminmax = np.array([sampleout.min(axis=1).T.tolist()[0],sampleout.max(axis=1).T.tolist()[0]]).transpose()#2*2，对应最大值最小值

#5*32
sampleinnorm = (2*(np.array(samplein.T)-sampleinminmax.transpose()[0])/(sampleinminmax.transpose()[1]-sampleinminmax.transpose()[0])-1).transpose()
#2*32
sampleoutnorm = (2*(np.array(sampleout.T).astype(float)-sampleoutminmax.transpose()[0])/(sampleoutminmax.transpose()[1]-sampleoutminmax.transpose()[0])-1).transpose()

#给输出样本添加噪音
noise = 0.03*np.random.rand(sampleoutnorm.shape[0],sampleoutnorm.shape[1])
sampleoutnorm += noise



# 训练次数
maxepochs = 1000
# 学习速率
learnrate = 0.035
# 误差率
errorfinal = 0.65*10**(-3)
#errorfinal = 0.05
# 数据量
samnum = 32
# 输入数
indim = 5
# 输出数
outdim = 2
hiddenunitnum = 7  # 3~10


w1 = 0.5*np.random.rand(hiddenunitnum,indim)-0.1
b1 = 0.5*np.random.rand(hiddenunitnum,1)-0.1
w2 = 0.5*np.random.rand(outdim,hiddenunitnum)-0.1
b2 = 0.5*np.random.rand(outdim,1)-0.1

errhistory = []

for i in range(maxepochs):
    hiddenout = logsig((np.dot(w1,sampleinnorm).transpose()+b1.transpose())).transpose()
    networkout = (np.dot(w2,hiddenout).transpose()+b2.transpose()).transpose()
    err = sampleoutnorm - networkout
    sse = sum(sum(err**2))

    errhistory.append(sse)
    if sse < errorfinal:
        break

    delta2 = err

    delta1 = np.dot(w2.transpose(),delta2)*hiddenout*(1-hiddenout)

    dw2 = np.dot(delta2,hiddenout.transpose())
    db2 = np.dot(delta2,np.ones((samnum,1)))

    dw1 = np.dot(delta1,sampleinnorm.transpose())
    db1 = np.dot(delta1,np.ones((samnum,1)))

    w2 += learnrate*dw2
    b2 += learnrate*db2

    w1 += learnrate*dw1
    b1 += learnrate*db1


    # print 'err',err,'w1=',w1,'w2=',w2,'b1=',b1,'b2=',b2

# 误差曲线图
errhistory10 = np.log10(errhistory)
minerr = min(errhistory10)
plt.plot(errhistory10)
plt.plot(range(0,i+1000,1000),[minerr]*len(range(0,i+1000,1000)))

ax=plt.gca()
ax.set_yticks([-2,-1,0,1,2,minerr])
ax.set_yticklabels([u'$10^{-2}$',u'$10^{-1}$',u'$1$',u'$10^{1}$',u'$10^{2}$',str(('%.4f'%np.power(10,minerr)))])
ax.set_xlabel('iteration')
ax.set_ylabel('error')
ax.set_title('Error History')
plt.savefig('errorhistory2.png',dpi=700)
plt.close()


# 仿真输出和实际输出对比图
hiddenout = logsig((np.dot(w1,sampleinnorm).transpose()+b1.transpose())).transpose()
networkout = (np.dot(w2,hiddenout).transpose()+b2.transpose()).transpose()
diff = sampleoutminmax[:,1]-sampleoutminmax[:,0]
networkout2 = (networkout+1)/2
networkout2[0] = networkout2[0]*diff[0]+sampleoutminmax[0][0]
networkout2[1] = networkout2[1]*diff[1]+sampleoutminmax[1][0]

sampleout = np.array(sampleout)

fig,axes = plt.subplots(nrows=2,ncols=1,figsize=(12,10))
line1, =axes[0].plot(networkout2[0],'k',marker = u'$\circ$')
line2, = axes[0].plot(sampleout[0],'r',markeredgecolor='b',marker = u'$\star$',markersize=9)

axes[0].legend((line1,line2),('simulation output','real output'),loc = 'upper left')

yticks = [0,100,200,300,400,500,600]
ytickslabel = [u'$0$',u'$100$',u'$200$',u'$300$',u'$400$',u'$500$',u'$600$']
axes[0].set_yticks(yticks)
axes[0].set_yticklabels(ytickslabel)
axes[0].set_ylabel('ordernum')

xticks = range(0,32,2)
xtickslabel = range(1,32,2)
axes[0].set_xticks(xticks)
axes[0].set_xticklabels(xtickslabel)
axes[0].set_xlabel(u'date')
axes[0].set_title('ordernum')
#ordernum


line3, = axes[1].plot(networkout2[1],'k',marker = u'$\circ$')
line4, = axes[1].plot(sampleout[1],'r',markeredgecolor='b',marker = u'$\star$',markersize=9)
axes[1].legend((line3,line4),('simulation output','real output'),loc = 'upper left')
yticks = [0,5000,10000,15000,20000,25000]
ytickslabel = [u'$0$',u'$5000$',u'$10000$',u'$15000$',u'$20000$',u'$25000$']
axes[1].set_yticks(yticks)
axes[1].set_yticklabels(ytickslabel)
axes[1].set_ylabel('tradesum')

xticks = range(0,32,2)
xtickslabel = range(1,32,2)
axes[1].set_xticks(xticks)
axes[1].set_xticklabels(xtickslabel)
axes[1].set_xlabel(u'date')
axes[1].set_title('tradesum')

fig.savefig('simulation2.png',dpi=500,bbox_inches='tight')
plt.close()