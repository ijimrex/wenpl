#encoding=utf-8
su = ["人生苦短"]
# ： su是一个utf-8格式的字节串
u  = su[0].decode("utf-8")
print u
# ： s被解码为unicode对象，赋给u
sg = u.encode("gbk")
# ： u被编码为gbk格式的字节串，赋给sg
print sg