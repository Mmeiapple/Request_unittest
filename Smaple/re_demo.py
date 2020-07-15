import re

# str = "newdream,com on!"
# str2 = "changsha2german3enlish"
#
# pattrrn = re.compile(r"newdream")  # 加了原生字符串
#
# result1 = re.match(pattrrn, str)  # 匹配以什么开头
# # print(result1[0])
#
# # 匹配单个单词
# pattrrn2 = re.compile(r"\w+")
# result2 = re.match(pattrrn2, str)  # 匹配以什么开头
# print(result2.group(0))
#
# pattrrn3 = re.compile(r"(\w+),(\w+) (\w+)(?P<sign>.*)")
# result3 = re.match(pattrrn3, str)  # 匹配以什么开头
# print(result3.group(0))
# # 取项任意排序
# print(result3.expand(r"\2 \3 \1 \4"))
#
# # 匹配以什么开头
# # pattrrn4=re.compile(r"newdream(\w+)！")
# # result4=re.search(pattrrn4,str)
# #
# # print(result4.group(0))
#
# # 分割
# pattrrn5 = re.compile(r"\d+")
# result5 = re.split(pattrrn5, str2)
# print(result5)
#
# # 列表形式返还能匹配到的
# pattrrn6 = re.compile(r"\d+")
# result6 = re.findall(pattrrn6, str2)
# print(result6)
#
# # 替换
#
# str3 = 'summer hot ~~'
# pattrrn6 = re.compile(r"(\w+) (\w+)")
# result6 = re.sub(pattrrn6, r"\2 \1", str3)
# print(result6)

#  匹配中文
# string = 'tom say:i love python,非常喜欢。'
#
# pattern = re.compile('[\u4e00-\u9fa5]+')
#
# res = re.search(pattern, string)
#
# print(res.group(0))

# search写法

# string = '我爱你 520 1314'
#
# pattern = re.compile(' \d\d\d \d\d\d\d')
#
# res = pattern.search(string).group()
#
# print(res)


# match写法

# string = '我爱你520 我爱你520'
#
# pattern = re.compile('我爱你\d20 我爱你5\d0')
#
# res = pattern.match(string).group()
#
# print(res)


# match

# hello前面的r的意思是“原生字符串”

# pattern = re.compile(r'hello')
#
# # 使用re.match匹配文本，获得匹配结果，无法匹配时将返回None
#
# result1 = pattern.match('hello')
#
# result2 = re.match(pattern,'helloo CQC!')
#
# result3 = re.match(pattern,'helo CQC!')
#
# result4 = re.match(pattern,'hello CQC!')
#
#
# if result1: #如果1匹配成功
#     print(result1.group())    # 使用Match获得分组信息
# else:
#     print("result1: 匹配失败！")
#
# if result2: #如果2匹配成功
#     print(result2.group())
#
# else:
#     print("result2: 匹配失败！")
#
# if result3:
#     print(result3.group())
# else:
#     print("result3: 匹配失败！")
#
# if result4:
#     print(result4.group())
# else:
#     print("result4: 匹配失败！")


# split

# string='test1 test2 test3'
#
# pattern = re.compile(r'\d+') #匹配1个或多个数字
#
# value = re.split(pattern,string)
#
#
# print()
# print(value)
#


string='testone1testtwo2testthree3'

pattern = re.compile(r'1(.+?)2') #匹配1个或多个数字

value = re.findall(pattern,string)


print()
print(value)
