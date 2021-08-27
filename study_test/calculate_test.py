import math

arr = [28.03, 28.01, 27.98, 27.94, 27.96, 28.02, 28.00, 27.93, 27.95, 27.90]
ans = 0
for i in arr:
    ans += i
ans /= len(arr)
print(ans)

list = []
for i in arr:
    list.append(i - ans)
print(list)

s1 = 0
s2 = 0
for i in range(5):
    #print(i)
    s1 += list[i]

for i in range(5, 10):
    #print(i)
    s2 += list[i]

print(s1)
print(s2)
print(s1-s2)

s3=0
for i in range(9):
    s3+=list[i]*list[i+1]
print(s3)

s4=0
for i in range(10):
    s4+=list[i]*list[i]

print(s4/10*3)
