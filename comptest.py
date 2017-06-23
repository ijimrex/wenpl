import re
sentence='2345678abcdef'
match = re.findall(r'^(?=.*a)(?=.*b)(?=.*c)(?=.*d)(?=.*e).*$', sentence)
print match

