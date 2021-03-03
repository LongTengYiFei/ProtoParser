# coding=utf-8
import sys
import math
import string
import struct
import copy

class ProtoParser:
    def __init__(self):
        self.proto_dict = {}
        self.bin_str = ''
        pass

    def reverse_string_2(self, s):
        # reverse string
        # step is 2
        i = len(s) - 2
        ans = ""
        while i >= 0:
            ans += s[i]
            ans += s[i + 1]
            i -= 2
        return ans

    # all the int8-32 in the python is int

    def bsey_to_digit(self, bsey):
        # 8421 code to a digit, 16 jin zhi
        if bsey == '0000':
            return '0'
        elif bsey == '0001':
            return '1'
        elif bsey == '0010':
            return '2'
        elif bsey == '0011':
            return '3'
        elif bsey == '0100':
            return '4'
        elif bsey == '0101':
            return '5'
        elif bsey == '0110':
            return '6'
        elif bsey == '0111':
            return '7'
        elif bsey == '1000':
            return '8'
        elif bsey == '1001':
            return '9'
        elif bsey == '1010':
            return 'a'
        elif bsey == '1011':
            return 'b'
        elif bsey == '1100':
            return 'c'
        elif bsey == '1101':
            return 'd'
        elif bsey == '1110':
            return 'e'
        elif bsey == '1111':
            return 'f'

    def Serialization_int8(self, n):
        if n > 127 or n < -128:
            raise Exception('error ,the int8 argument is not valid')
        ans = bin(n & 0xff)
        ans = ans[2:]
        rest = 8 - len(ans)
        # print(rest)
        for i in range(rest):
            ans = '0' + ans
        # slice,left close, right open
        left = ans[0:4]
        right = ans[4:]
        ans = self.bsey_to_digit(left) + self.bsey_to_digit(right)
        return ans

    def Serialization_uint8(self, n):
        if n > 0xff or n < 0:
            raise Exception('error ,the uint8 argument is not valid')
        tmp = hex(n)
        tmp = tmp[2:]
        if len(tmp) == 1:
            return '0' + tmp
        return tmp

    def Serialization_int16(self, n):
        if n > 32767 or n < -32768:
            raise Exception('error ,the int16 argument is not valid')
        ans = bin(n & 0xffff)
        ans = ans[2:]
        rest = 16 - len(ans)
        # print(rest)
        for i in range(rest):
            ans = '0' + ans

        tmp = ''
        for i in range(16 / 4):
            bsey = ans[i * 4:i * 4 + 4]
            tmp += self.bsey_to_digit(bsey)

        tmp = self.reverse_string_2(tmp)
        return tmp

    def Serialization_uint16(self, n):
        if n > 0xffff or n < 0:
            raise Exception('error ,the uint16 argument is not valid')
        tmp = hex(n)
        tmp = tmp[2:]
        if len(tmp) == 1:
            tmp = '000' + tmp
        elif len(tmp) == 2:
            tmp = '00' + tmp
        elif len(tmp) == 3:
            tmp = '0' + tmp

        tmp = self.reverse_string_2(tmp)
        return tmp

    def Serialization_int32(self, n):
        if n > 2147483647 or n < -2147483648:
            raise Exception('error ,the int32 argument is not valid')
        ans = bin(n & 0xffffffff)
        ans = ans[2:]
        rest = 32 - len(ans)
        # print(rest)
        for i in range(rest):
            ans = '0' + ans

        tmp = ''
        for i in range(32 / 4):
            bsey = ans[i * 4:i * 4 + 4]
            tmp += self.bsey_to_digit(bsey)

        tmp = self.reverse_string_2(tmp)
        return tmp

    def Serialization_uint32(self, n):
        if n > 0xffffffff or n < 0:
            raise Exception('error ,the uint32 argument is not valid')
        tmp = hex(n)
        tmp = tmp[2:]
        if len(tmp) == 1:
            tmp = '0000000' + tmp
        elif len(tmp) == 2:
            tmp = '000000' + tmp
        elif len(tmp) == 3:
            tmp = '00000' + tmp
        elif len(tmp) == 4:
            tmp = '0000' + tmp
        elif len(tmp) == 5:
            tmp = '000' + tmp
        elif len(tmp) == 6:
            tmp = '00' + tmp
        elif len(tmp) == 7:
            tmp = '0' + tmp

        tmp = self.reverse_string_2(tmp)
        return tmp

    def Serialization_float(self, f):
        f = float(f)
        tmp = hex(struct.unpack('<L', struct.pack('<f', f))[0])
        # don't get the first 0x
        tmp = tmp[2:]
        # supply the high position zero
        rest = 8 - len(tmp)
        for i in range(rest):
            tmp = '0' + tmp
        # reverse , step is 2
        ans = self.reverse_string_2(tmp)
        return ans

    def Serialization_double(self, d):
        ans = struct.pack('<d', d).encode('hex')
        return ans
        '''
        d = float(d)
        tmp = hex(struct.unpack('<Q', struct.pack('<d', d))[0])
        # don't get the first 0x
        tmp = tmp[2:]
        # supply the high position zero
        rest = 16 - len(tmp)
        for i in range(rest):
            tmp = '0' + tmp
        # reverse , step is 2
        ans = self.reverse_string_2(tmp)
        return ans
        '''

    def Serialization_bool(self, flag):
        if flag == True:
            return '01'
        else:
            return '00'

    def Serialization_string(self, s):
        # first Serialize the len
        string_len = len(s)
        ans = ""
        ans += self.Serialization_uint16(string_len)
        # then Serialize the content
        for c in s:
            ans += hex(ord(c))[2:]
        return ans

    # 注意，这里数组里面永远不可能是dict，因为dict数组在序列化dict里面处理
    # 这是因为我把字典数组也解析成了字典
    def Serialization_fixed_tuple(self, T, proto_type):
        # fixed tuple don't need Serialize the len
        # straight Serialize the content
        # print("come into serilia fix tuple")
        # print("proto type is ", proto_type)
        # print("T is", T)
        # print("T's type is", type(T))

        if type(T) != tuple:
            raise Exception("传入的T不是元组！")

        # -------------
        ans = ""
        for t in T:
            if proto_type == 'int8':
                ans += self.Serialization_int8(t)
            elif proto_type == 'uint8':
                ans += self.Serialization_uint8(t)
            elif proto_type == 'int16':
                ans += self.Serialization_int16(t)
            elif proto_type == 'uint16':
                ans += self.Serialization_uint16(t)
            elif proto_type == 'int32':
                ans += self.Serialization_int32(t)
            elif proto_type == 'uint32':
                ans += self.Serialization_uint32(t)
            elif proto_type == 'float':
                ans += self.Serialization_float(t)
            elif proto_type == 'double':
                ans += self.Serialization_double(t)
            elif proto_type == 'fixed_tuple':
                ans += self.Serialization_fixed_tuple(t)
            elif proto_type == 'varied_tuple':
                ans += self.Serialization_varied_tuple(t)
            elif proto_type == 'string':
                ans += self.Serialization_string(t)
            elif proto_type == 'bool':
                ans += self.Serialization_bool(t)
        return ans

    def Serialization_varied_tuple(self, T, proto_type):
        # first Serialize the len
        ans = ""
        vt_len = len(T)
        ans += self.Serialization_uint16(vt_len)
        # then Serialize the content
        for t in T:
            if proto_type == 'int8':
                ans += self.Serialization_int8(t)
            elif proto_type == 'uint8':
                ans += self.Serialization_uint8(t)
            elif proto_type == 'int16':
                ans += self.Serialization_int16(t)
            elif proto_type == 'uint16':
                ans += self.Serialization_uint16(t)
            elif proto_type == 'int32':
                ans += self.Serialization_int32(t)
            elif proto_type == 'uint32':
                ans += self.Serialization_uint32(t)
            elif proto_type == 'float':
                ans += self.Serialization_float(t)
            elif proto_type == 'double':
                ans += self.Serialization_double(t)
            elif proto_type == 'fixed_tuple':
                ans += self.Serialization_fixed_tuple(t)
            elif proto_type == 'varied_tuple':
                ans += self.Serialization_varied_tuple(t)
            elif proto_type == 'string':
                ans += self.Serialization_string(t)
            elif proto_type == 'bool':
                ans += self.Serialization_bool(t)
        return ans

    def Serialization_dict(self, d, proto_dict):
        # 注意，有可能proto dict不是空的，但是你传进来的obj是空的，这时怎么序列化？

        # 对于字典的复制一定要用深拷贝，否则序列化之后的协议字典已经变了！
        ans = ""
        # print('进入字典序列化')
        # print(proto_dict['len'])
        # print(proto_dict)
        # 如果这个字典是定长的，那么也得循环序列化，只不过不用序列化长度
        # 注意，定长字典在python内部是数组
        # 定长数组长度大于等于0，和题目描述的不一样
        if proto_dict['len'] >= 0:
            sub_proto = copy.deepcopy(proto_dict)
            # 把每个子协议都当成单个字典再递归调用序列化字典
            # 长度为-1代表单个字典
            sub_proto['len'] = -1
            for i in range(proto_dict['len']):
                # 每个子协议是相同的，因为这是字典数组
                pass
            pass
        # 单个字典序列化
        for tu in proto_dict['content']:
            # 先做单个元素的判断
            if tu[0] == 'string':
                ans += self.Serialization_string(d[tu[1]])
            elif tu[0] == 'int8':
                ans += self.Serialization_int8(d[tu[1]])
            elif tu[0] == 'int16':
                ans += self.Serialization_int16(d[tu[1]])
            elif tu[0] == 'int32':
                ans += self.Serialization_int32(d[tu[1]])
            elif tu[0] == 'uint8':
                ans += self.Serialization_uint8(d[tu[1]])
            elif tu[0] == 'uint16':
                ans += self.Serialization_uint16(d[tu[1]])
            elif tu[0] == 'uint32':
                ans += self.Serialization_uint32(d[tu[1]])
            elif tu[0] == 'bool':
                ans += self.Serialization_bool(d[tu[1]])
            elif tu[0] == 'float':
                ans += self.Serialization_float(d[tu[1]])
            elif tu[0] == 'double':
                ans += self.Serialization_double(d[tu[1]])
            # 再来变长数组的判断
            elif tu[0] == 'string[]':
                ans += self.Serialization_varied_tuple(d[tu[1]], 'string')
            elif tu[0] == 'int8[]':
                ans += self.Serialization_varied_tuple(d[tu[1]], 'int8')
            elif tu[0] == 'int16[]':
                ans += self.Serialization_varied_tuple(d[tu[1]], 'int16')
            elif tu[0] == 'int32[]':
                ans += self.Serialization_varied_tuple(d[tu[1]], 'int32')
            elif tu[0] == 'uint8[]':
                ans += self.Serialization_varied_tuple(d[tu[1]], 'uint8')
            elif tu[0] == 'uint16[]':
                ans += self.Serialization_varied_tuple(d[tu[1]], 'uint16')
            elif tu[0] == 'uint32[]':
                ans += self.Serialization_varied_tuple(d[tu[1]], 'uint32')
            elif tu[0] == 'float[]':
                ans += self.Serialization_varied_tuple(d[tu[1]], 'float')
            elif tu[0] == 'double[]':
                ans += self.Serialization_varied_tuple(d[tu[1]], 'double')
            elif tu[0] == 'bool[]':
                ans += self.Serialization_varied_tuple(d[tu[1]], 'bool')
            # 再来定长数组判断
            elif tu[0][0:7] == 'string[':
                ans += self.Serialization_fixed_tuple(d[tu[1]], 'string')
            elif tu[0][0:6] == 'float[':
                ans += self.Serialization_fixed_tuple(d[tu[1]], 'float')
            elif tu[0][0:7] == 'double[':
                ans += self.Serialization_fixed_tuple(d[tu[1]], 'double')
            elif tu[0][0:5] == 'bool[':
                ans += self.Serialization_fixed_tuple(d[tu[1]], 'bool')
            elif tu[0][0:5] == 'int8[':
                ans += self.Serialization_fixed_tuple(d[tu[1]], 'int8')
            elif tu[0][0:6] == 'int16[':
                ans += self.Serialization_fixed_tuple(d[tu[1]], 'int16')
            elif tu[0][0:6] == 'int32[':
                ans += self.Serialization_fixed_tuple(d[tu[1]], 'int32')
            elif tu[0][0:6] == 'uint8[':
                ans += self.Serialization_fixed_tuple(d[tu[1]], 'uint8')
            elif tu[0][0:7] == 'uint16[':
                ans += self.Serialization_fixed_tuple(d[tu[1]], 'uint16')
            elif tu[0][0:7] == 'uint32[':
                ans += self.Serialization_fixed_tuple(d[tu[1]], 'uint32')
            # 最后是字典的判断
            elif tu[0][0:4] == 'dict':
                sub_proto_dict = tu[1]
                sub_dict = d[tu[1]['name']]
                # print(sub_proto_dict['len'])
                # print('sub_proto_dict')
                # print(sub_proto_dict)
                # print('sub_dict')
                # print(sub_dict)
                # 你从协议里面解析出来的字典有可能是字典数组！所以sub_dict的类型不一定是字典
                # sub_dict的类型有可能是定长或者变长数组！
                if sub_proto_dict['len'] == -1:
                    ans += self.Serialization_dict(sub_dict, sub_proto_dict)
                # 注意，剩下两种情况的sub_dict并不是dict，而是tuple
                elif sub_proto_dict['len'] == -2:
                    # 变长数组需要先序列化长度
                    # print('变长')
                    # print(len(sub_dict))
                    ans += self.Serialization_uint16(len(sub_dict))
                    xun_huan_proto = copy.deepcopy(sub_proto_dict)
                    xun_huan_proto['len'] = -1
                    for tt in sub_dict:
                        ans += self.Serialization_dict(tt, xun_huan_proto)
                    pass
                elif sub_proto_dict['len'] >= 0:
                    # 定长数组不用序列化长度
                    # print('定长')
                    # print(len(sub_dict))
                    xun_huan_proto = copy.deepcopy(sub_proto_dict)
                    xun_huan_proto['len'] = -1
                    for tt in sub_dict:
                        ans += self.Serialization_dict(tt, xun_huan_proto)
        return ans

    '''
    反       序       列       化
    '''

    # 协议字典里面的content是元组序列，根据元组的第一个值（就是类型），计算要从bin_str截取多长
    def get_len(self, tu):
        # 可能的长度，bin_str开头的4个字符
        maybe_len = self.Deserialization_uint16(self.bin_str[0:4])
        if tu[0] == 'int8' or tu[0] == 'uint8' or tu[0] == 'bool':
            return 2
        if tu[0] == 'int16' or tu[0] == 'uint16':
            return 4
        if tu[0] == 'int32' or tu[0] == 'uint32' or tu[0] == 'float':
            return 8
        if tu[0] == 'double':
            return 16

        if tu[0] == 'int8[]' or tu[0] == 'uint8[]' or tu[0] == 'bool[]':
            return 2 * maybe_len
        if tu[0] == 'int16[]' or tu[0] == 'uint16[]':
            return 4 * maybe_len
        if tu[0] == 'int32[]' or tu[0] == 'uint32[]' or tu[0] == 'float[]':
            return 8 * maybe_len
        if tu[0] == 'double[]':
            return 16 * maybe_len

    def Deserialization_uint8(self, s):
        return struct.unpack('<B', s.decode('hex'))[0]

    def Deserialization_uint16(self, s):
        return struct.unpack('<H', s.decode('hex'))[0]

    def Deserialization_uint32(self, s):
        return struct.unpack('<I', s.decode('hex'))[0]

    def Deserialization_int8(self, s):
        return struct.unpack('<b', s.decode('hex'))[0]

    def Deserialization_int16(self, s):
        return struct.unpack('<h', s.decode('hex'))[0]

    def Deserialization_int32(self, s):
        return struct.unpack('<i', s.decode('hex'))[0]

    def Deserialization_bool(self, s):
        if s == '01':
            return True
        else:
            return False

    def Deserialization_float(self, s):
        return struct.unpack('<f', s.decode('hex'))[0]

    def Deserialization_double(self, s):
        try:
            ans = struct.unpack('<d', s.decode('hex'))[0]
        except UnicodeDecodeError:
            raise Exception("UnicodeDecodeError------")
        else:
            return ans

    def Deserialization_string(self, s):
        # print(s)
        s = s[4:]
        # 在s的每两个字符前面插入'/x'
        tmp = ''
        i = 0
        while i <= len(s) - 1:
            tmp += '/x'
            tmp += s[i]
            tmp += s[i + 1]
            i += 2
        # 网上百度的输入是每两个字符前面有/x，所以用他的就得自己插入
        return ''.join([chr(i) for i in [int(b, 16) for b in tmp.split(r'/x')[1:]]])

    # 反序列化字典的时候就一点一点过滤，没必要提前知道整个字典的长度，反正序列化的时候也是顺序序列化的
    # 我有一个本对象的全局bin-str，代表剩下的还没反序列化的binstr
    # binstr和proto-dict都是类对象的成员变量
    def Deserialization_dict(self, sub_dict):
        # print(sub_dict)
        ans = {}
        for tu in sub_dict['content']:
            # print(tu)
            if tu[0] == 'string':
                str_len = self.Deserialization_uint16(self.bin_str[0:4])
                ans_key = tu[1]
                ans_value = self.Deserialization_string(self.bin_str[0:4+str_len*2])
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[4+str_len*2:]
            elif tu[0] == 'double':
                ans_key = tu[1]
                ans_value = self.Deserialization_double(self.bin_str[0:16])
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[16:]
            elif tu[0] == 'float':
                ans_key = tu[1]
                ans_value = self.Deserialization_float(self.bin_str[0:8])
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[8:]
            elif tu[0] == 'int8':
                ans_key = tu[1]
                ans_value = self.Deserialization_int8(self.bin_str[0:2])
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[2:]
            elif tu[0] == 'int16':
                ans_key = tu[1]
                ans_value = self.Deserialization_int16(self.bin_str[0:4])
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[4:]
            elif tu[0] == 'int32':
                ans_key = tu[1]
                ans_value = self.Deserialization_int32(self.bin_str[0:8])
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[8:]
            elif tu[0] == 'uint8':
                ans_key = tu[1]
                ans_value = self.Deserialization_uint8(self.bin_str[0:2])
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[2:]
            elif tu[0] == 'uint16':
                ans_key = tu[1]
                ans_value = self.Deserialization_uint16(self.bin_str[0:4])
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[4:]
            elif tu[0] == 'uint32':
                ans_key = tu[1]
                ans_value = self.Deserialization_uint32(self.bin_str[0:8])
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[8:]
            elif tu[0] == 'bool':
                ans_key = tu[1]
                ans_value = self.Deserialization_bool(self.bin_str[0:2])
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[2:]

            # 变长数组判断
            elif tu[0] == 'string[]':
                tuple_len = self.Deserialization_uint16(self.bin_str[0:4])
                self.bin_str = self.bin_str[4:]
                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    str_len = self.Deserialization_uint16(self.bin_str[0:4])

                    ans_value.append(self.Deserialization_string(self.bin_str[0:4 + 2 * str_len]))
                    self.bin_str = self.bin_str[4 + 2 * str_len:]  # 截断
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
            elif tu[0] == 'double[]':
                tuple_len = self.Deserialization_uint16(self.bin_str[0:4])
                self.bin_str = self.bin_str[4:]
                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_double(self.bin_str[i * 16:i * 16 + 16]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[16 * tuple_len:]
            elif tu[0] == 'float[]':
                tuple_len = self.Deserialization_uint16(self.bin_str[0:4])
                self.bin_str = self.bin_str[4:]
                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_float(self.bin_str[i * 8:i * 8 + 8]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[8 * tuple_len:]
            elif tu[0] == 'int8[]':
                tuple_len = self.Deserialization_uint16(self.bin_str[0:4])
                self.bin_str = self.bin_str[4:]
                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_int8(self.bin_str[i * 2:i * 2 + 2]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[2 * tuple_len:]
            elif tu[0] == 'int16[]':
                tuple_len = self.Deserialization_uint16(self.bin_str[0:4])
                self.bin_str = self.bin_str[4:]
                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_int16(self.bin_str[i * 4:i * 4 + 4]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[4 * tuple_len:]
            elif tu[0] == 'int32[]':
                # 注意，这里的and-value是元组，元组的长度就是tuple-len
                # ans-value先用列表，后序再转元组
                tuple_len = self.Deserialization_uint16(self.bin_str[0:4])
                # 去掉长度，反正已经拿到手了
                self.bin_str = self.bin_str[4:]
                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_int32(self.bin_str[i*8:i*8+8]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[8*tuple_len:]
            elif tu[0] == 'uint8[]':
                tuple_len = self.Deserialization_uint16(self.bin_str[0:4])
                self.bin_str = self.bin_str[4:]
                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_uint8(self.bin_str[i * 2:i * 2 + 2]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[2 * tuple_len:]
            elif tu[0] == 'uint16[]':
                tuple_len = self.Deserialization_uint16(self.bin_str[0:4])
                self.bin_str = self.bin_str[4:]
                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_uint16(self.bin_str[i * 4:i * 4 + 4]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[4 * tuple_len:]
            elif tu[0] == 'uint32[]':
                tuple_len = self.Deserialization_uint16(self.bin_str[0:4])
                self.bin_str = self.bin_str[4:]
                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_uint32(self.bin_str[i * 8:i * 8 + 8]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[8 * tuple_len:]
            elif tu[0] == 'bool[]':
                tuple_len = self.Deserialization_uint16(self.bin_str[0:4])
                self.bin_str = self.bin_str[4:]
                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_bool(self.bin_str[i * 2:i * 2 + 2]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[2 * tuple_len:]
            # 定长数组判断-----------------------
            # 定长数组和变长数组的区别就是
            # 定长数组的长度再tu[0]里面包括了
            # 变长数组的长度再binstr里面
            elif tu[0][0:7] == 'string[':
                tuple_len = tu[0][7:-1]
                tuple_len = int(tuple_len)
                ans_key = tu[1]
                ans_value = []
                # 注意，每个string也是可变的，所以你循环的时候也要把binstr截短,而不能等到循环结束再截断
                for i in range(tuple_len):
                    str_len = self.Deserialization_uint16(self.bin_str[0:4])
                    ans_value.append(self.Deserialization_string(self.bin_str[0:4+2*str_len]))
                    self.bin_str = self.bin_str[4+2*str_len]# 截断
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
            elif tu[0][0:7] == 'double[':
                tuple_len = tu[0][7:-1]
                tuple_len = int(tuple_len)

                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_double(self.bin_str[i * 16:i * 16 + 16]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[16 * tuple_len:]
            elif tu[0][0:6] == 'float[':
                tuple_len = tu[0][6:-1]
                tuple_len = int(tuple_len)
                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_float(self.bin_str[i * 8:i * 8 + 8]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[8 * tuple_len:]
            elif tu[0][0:5] == 'int8[':
                tuple_len = tu[0][5:-1]
                tuple_len = int(tuple_len)
                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_int8(self.bin_str[i * 2:i * 2 + 2]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[2 * tuple_len:]
            elif tu[0][0:6] == 'int16[':
                tuple_len = tu[0][6:-1]
                tuple_len = int(tuple_len)

                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_int16(self.bin_str[i * 4:i * 4 + 4]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[4 * tuple_len:]
            elif tu[0][0:6] == 'int32[':
                tuple_len = tu[0][6:-1]
                tuple_len = int(tuple_len)

                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_int32(self.bin_str[i * 8:i * 8 + 8]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[8 * tuple_len:]
            elif tu[0][0:6] == 'uint8[':
                tuple_len = tu[0][6:-1]
                tuple_len = int(tuple_len)

                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_uint8(self.bin_str[i * 2:i * 2 + 2]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[2 * tuple_len:]
            elif tu[0][0:7] == 'uint16[':
                tuple_len = tu[0][7:-1]
                tuple_len = int(tuple_len)

                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_uint16(self.bin_str[i * 4:i * 4 + 4]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[4 * tuple_len:]
            elif tu[0][0:7] == 'uint32[':
                tuple_len = tu[0][7:-1]
                tuple_len = int(tuple_len)

                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_uint32(self.bin_str[i * 8:i * 8 + 8]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[8 * tuple_len:]
            elif tu[0][0:5] == 'bool[':
                tuple_len = tu[0][5:-1]
                tuple_len = int(tuple_len)
                ans_key = tu[1]
                ans_value = []
                for i in range(tuple_len):
                    ans_value.append(self.Deserialization_bool(self.bin_str[i * 2:i * 2 + 2]))
                ans_value = tuple(ans_value)
                ans[ans_key] = ans_value
                self.bin_str = self.bin_str[2 * tuple_len:]
            # 字典包括了单个字典，变长字典，定长字典三种情况
            # 这是由于我的协议字典解析方式
            # 变长字典数组和定长字典数组的区别就是长度获取方式不一样
            elif tu[0][0:4] == 'dict':
                # tu[1]是子协议字典
                ans_key = tu[1]['name']
                if tu[1]['len'] == -1:
                    ans_value = self.Deserialization_dict(tu[1])
                    ans[ans_key] = ans_value

                elif tu[1]['len'] == -2:
                    # 变长字典数组
                    tuple_len = self.Deserialization_uint16(self.bin_str[0:4])
                    self.bin_str = self.bin_str[4:]

                    ans_value = []
                    for i in range(tuple_len):
                        ans_value.append(self.Deserialization_dict(tu[1]))
                    ans_value = tuple(ans_value)
                    ans[ans_key] = ans_value
                else:
                    # 定长字典数组
                    tuple_len = tu[1]['len']

                    ans_value = []
                    for i in range(tuple_len):
                        ans_value.append(self.Deserialization_dict(tu[1]))
                    ans_value = tuple(ans_value)
                    ans[ans_key] = ans_value

            elif tu[0] == '':
                return ans
            else:
                raise Exception('error ,deserialize dict')
        return ans

    '''
    保存dict
    键就是dict或者dict[]或者dict[n],n是数字
    值是一个二元tuple，第一个值是dict的name，第二个值是一个字典（保存dict的格式）
    '''
    '''
    注意到，我这个解析的字典里面的键name和len永远也不会和用户的冲突
    因为用户的键只有
    int8	int
    uint8	int
    int16	int
    uint16	int
    int32	int
    uint32	int
    float	float
    double	float
    bool	True/False
    string	str (utf-8)
    数组	tuple
    组合 dict
    '''

    # 比如进来'stringname' ，返回一个二元tuple('string', 'name')
    # 比如进来'int32id', 返回一个二元tuple('int32', 'id')
    # 比如进来'int32[]friends',返回('int32[]', 'friends')
    def divide_raw(self, raw):
        # print(raw)
        ans = ('', '')
        i = len(raw) - 1
        while i >= 0:
            if raw[i] == ']':
                break
            i -= 1
        if i >= 0:
            return (raw[0:i + 1], raw[i + 1:])
        else:
            # print(i)
            if raw[0:6] == 'string':
                ans = ('string', raw[6:])
            if raw[0:4] == 'bool':
                ans = ('bool', raw[4:])
            if raw[0:6] == 'double':
                ans = ('double', raw[6:])
            if raw[0:5] == 'float':
                ans = ('float', raw[5:])
            if raw[0:6] == 'uint32':
                ans = ('uint32', raw[6:])
            if raw[0:5] == 'int32':
                ans = ('int32', raw[5:])
            if raw[0:6] == 'uint16':
                ans = ('uint16', raw[6:])
            if raw[0:5] == 'int16':
                ans = ('int16', raw[5:])
            if raw[0:5] == 'uint8':
                ans = ('uint8', raw[5:])
            if raw[0:4] == 'int8':
                ans = ('int8', raw[4:])
        return ans

    # 这个函数根据我们给出的左括号的位置，寻找匹配的右括号的位置
    def find_right_class(self, content, left):
        sta = []
        i = left
        sta.append(content[left])
        i += 1
        while i < len(content):
            if content[i] == '{':
                sta.append('{')
            elif content[i] == '}':
                sta.pop()
                if len(sta) == 0:
                    # print(i)
                    return i
            i += 1

    def build_proto(self, content):
        # 变量名符合c语言规则，那就只包括数字 /字母 /下划线
        # 测试用例F协议里面有逗号分隔符，那我把逗号全部替换成分号不就行了？
        content = content.replace(',', ';')

        # 去掉所有的空格和换行
        content = content.replace(' ', '')
        content = content.replace('\n', '')
        content = content.replace('\t', '')

        # print('去掉空格和换行'+content)
        # 如果len等于-1那么就是单个字典
        # 如果len等于0那么就是变长字典
        # 如果len大于0，那么就是定长字典
        my_dict = {
            'name': '',
            'len': -1,
            'content': []
        }
        # 首先，我这个content一定是一个字典，这是调用者确保的
        # 就是说结尾一定是分号
        # 然后结尾的分号前面就是name

        # 由于过滤了空格和换行符
        # 第一个左括号的位置一定是0！
        left_class = 0
        right_class = self.find_right_class(content, left_class)
        # 如果第一个右括号的左边不是分号，那就意味着最后一个变量不是以分号结尾的，我就补一个分号，方便后面解析
        # 奇怪的是py2的字符串没有insert，我只能把左右拆开，再往左边的末尾添加一个分号，再合并左右
        if content[right_class-1] != ';':
            content_left = content[0:right_class]
            content_left = content_left+';'
            content_right = content[right_class:]
            content = content_left + content_right
            right_class += 1 # 注意，我添加了一个分号，右括号的位置也向右移动了一个

        my_dict['name'] = content[right_class + 1:-1]
        # print(my_dict['name'])

        # 我们解析一个字典时，它内部可能还有若干个字典
        # 先把内部字典编号初始化为1
        dict_num = 1
        # print(right_class)
        i = 0
        while i <= right_class - 1:
            # print(i)
            # rint(content[i])
            # 第一个字符一定是左大括号，跳过就行
            if content[i] == '{' and i == 0:
                i += 1
            elif content[i] == '{' and i != 0:
                # print(i)
                # 找到一个左括号，先找对应的右括号
                right_cla = self.find_right_class(content, i)
                # 从右括号往右找，找到第一个分号
                j = right_cla
                while j < len(content):
                    if content[j] == ';':
                        break;
                    j += 1
                sub_content = content[i:j + 1]
                my_dict['content'].append(('dict' + str(dict_num), self.build_proto(sub_content)))
                dict_num += 1
                i = j + 1
            elif content[i] == ';':
                # 往左找，找到第一个分号或者第一个左括号
                k = i - 1
                while content[k] != ';' and content[k] != '{':
                    k -= 1
                raw = content[k + 1:i]
                # print(raw)
                my_dict['content'].append(self.divide_raw(raw))
                i += 1
            else:
                i += 1
        # 现在的到的name有可能是pet或者[]pet或者[12]pet
        #  根据name的头部改变len

        # 变长
        # 由于定长数组长度可能为0，所以不能把变长数组设为0以表特殊
        # 那我就设-2
        if my_dict['name'][0:1] == '[' and my_dict['name'][1:2] == ']':
            my_dict['len'] = -2

        # 定长
        # 定长数组可能长度为0
        elif my_dict['name'][0:1] == '[' and my_dict['name'][1:2] != ']':
            tmp = ''
            for c in my_dict['name']:
                if c == '[':
                    pass
                elif c == ']':
                    break
                else:
                    tmp += c
            my_dict['len'] = int(tmp)

        # 单个
        else:
            my_dict['len'] = -1

        # print(my_dict['len'])
        # 现在name的头部已经没用了，舍弃
        for ii in range(len(my_dict['name'])):
            if my_dict['name'][ii] == ']':
                my_dict['name'] = my_dict['name'][ii + 1:]
                break
        return my_dict

    def buildDesc(self, filename):
        f = open(filename)
        content = f.read()
        content += 'root;'
        self.proto_dict = self.build_proto(content)
        # 如果len等于-1那么就是单个字典
        # 如果len等于0那么就是变长字典
        # 如果len大于0，那么就是定长字典
        '''
        proto的内容
        {
            'name':'root',
            'len': n,
            'content' : [(,),(,)...]
        }
        '''
# 即使是序列化也需要解析proto文件
# attention,the dict is unordered, serialize is also need analyze the proto file
    def dumps(self, d):
        return self.Serialization_dict(d, self.proto_dict)

    def loads(self, s):
        self.bin_str = s
        return self.Deserialization_dict(self.proto_dict)
    #------------


