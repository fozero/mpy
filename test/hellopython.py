# coding:utf-8

class Hello(object):
    def __init__(self):
        print 'hello python'

    def calc(self,a,b):
        print a + b

if __name__ == "__main__":
    hello = Hello()
    hello.calc(1,1)