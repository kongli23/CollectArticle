import re

string = 'a.quick-brown_fox+fox*jump'
arr = [str(i) for i in range(10, 0, -1)]
s1 = re.sub('\w+', lambda m: arr.pop(), string)
print(s1)