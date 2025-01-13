import re
help = """
^ 匹配字符串开头
$ 匹配字符串末尾
[] 匹配括号内任意其中一个字符
\d  匹配数字.  0-9
\D 匹配任意非数字 等价于[^0-9]
\w 匹配任意一个字符  a-zA-Z0-9
\W 匹配任意非字符  等价于[^a-zA-Z0-9]
+ 匹配一个或者多个，但是至少是一个
？ 匹配0个或者多个，可以是0个
{n} 匹配前面的表达式n个
{n，m} 匹配前面的表达式n到m个
"""
help_commend = """
re.search()  搜索，开头匹配
re.compile() 开头匹配
re.split()  按照正则表达式的方式进行切割  类似于字符串.split()
re.sub()  按照正则表达式的方式进项截取  类似于字符串.sub()
"""

#读取文件
dict_ = {}
with open('re.txt','r',encoding='utf8') as f:
    data = f.read()
for i in data:
    if dict_.get(i.lower(),-1) == -1:
        dict_[i.lower()] = 0
    else:
        dict_[i.lower()] += 1
# 按值升序排序
sorted_dict = dict(
    sorted(dict_.items(), key=lambda item: item[1],reverse=True)
)
print(sorted_dict)