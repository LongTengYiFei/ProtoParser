# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from ProtoParser import *
# Press the green button in the gutter to run the script.
'''
测试用例 f协议要求满足逗号分割，这可以吗？
'''

if __name__ == '__main__':
    pass
    # a ok
    # b ok
    # c ok
    # d ok
    # e ok
    # f ok
    # g ok 可以和e共用一个obj
    # h ok
    filename = "test.proto"
    a1 = ProtoParser()
    a1.buildDesc(filename)
    # print(a1.proto_dict)
    obj = {
       "angel": (-123,)
    }

    binstr = a1.dumps(obj)
    print("binstr = ", binstr)

    a2 = ProtoParser()
    a2.buildDesc(filename)
    result = a2.loads(binstr)
    print("result = ", result)






