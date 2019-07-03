from random import randint

list = [87, 107, 34, 104, 92, 106, 146, 72, 161, 81, 140, 172, 171, 178, 126, 104, 68, 133, 179, 136, 101, 94, 137, 94, 220, 179, 219, 128, 121, 44, 95, 78, 162]
chunks = [list[x:x+10] for x in range(0,len(list),10)]
print(chunks)