multtotal = 0

for i in range(1,1000001):
    if i % 3 == 0 and i % 5 ==0:
        multtotal += int(i)
print(multtotal)

