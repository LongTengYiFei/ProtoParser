# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from ProtoParser import *
# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    # 这个字典是我们想序列化的对象，要严格和协议文本里面的字段对应
    # 否则会出错。
    obj = {
        "name": "张三",
        "id": 5201314,
        "married": False,
        "friends": (5201315, 244578811),
        "position": (134.5, 0.0, 23.41),
        "pet": {
            "name": "张三的小可爱",
            "skill": (
                {
                    "id": 1,
                },
                {
                    "id": 2,
                })
        }
    }
    # 这是协议文本
    filename = "protos/a.proto"

    # 序列化步骤
    # 第一步：创建一个解析器实体
    a1 = ProtoParser()
    # 第二步：传入一个文件名，这个文件是文本文件，就是我们自定义的协议
    a1.buildDesc(filename)
    # 第三步：将一个字典对象传入dump方法，返回一个字符串，这个字符串就是序列化后的结果
    binstr = a1.dumps(obj)

    print("binstr = ", binstr)

    # 反序列化步骤
    # 第一步：同样创建一个解析器实体
    a2 = ProtoParser()
    # 第二步：反序列化也需要解析协议文件，必须传入相同的协议文件，因为本程序还不够健壮，
    # 如果传入不同的协议文件，后续的行为都是不可预知的。
    a2.buildDesc(filename)
    # 第三步，将一个字符串传入loads方法，返回一个字典对象，就是反序列化后的结果。
    result = a2.loads(binstr)

    print("result = ", result)






