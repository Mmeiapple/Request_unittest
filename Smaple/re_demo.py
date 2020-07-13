import re

str="newdream,com on!"
str2="changsha2german3enlish"

pattrrn=re.compile(r"newdream")#加了原生字符串

result1=re.match(pattrrn,str) # 匹配以什么开头
# print(result1[0])

# 匹配单个单词
pattrrn2=re.compile(r"\w+")
result2=re.match(pattrrn2,str) # 匹配以什么开头
print(result2.group(0))





pattrrn3=re.compile(r"(\w+),(\w+) (\w+)(?P<sign>.*)")
result3=re.match(pattrrn3,str) # 匹配以什么开头
print(result3.group(0))
#取项任意排序
print(result3.expand(r"\2 \3 \1 \4"))


#匹配以什么开头
# pattrrn4=re.compile(r"newdream(\w+)！")
# result4=re.search(pattrrn4,str)
#
# print(result4.group(0))

#分割
pattrrn5=re.compile(r"\d+")
result5=re.split(pattrrn5,str2)
print(result5)

#列表形式返还能匹配到的
pattrrn6=re.compile(r"\d+")
result6=re.findall(pattrrn6,str2)
print(result6)


#替换

str3='summer hot ~~'
pattrrn6=re.compile(r"(\w+) (\w+)")
result6=re.sub(pattrrn6,r"\2 \1",str3)
print(result6)




