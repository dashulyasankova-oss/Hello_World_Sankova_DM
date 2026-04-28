a = input("Введите число: ")
b = input("Введите число: ")
c = input("Введите ещё одно число: ")
d = input("Введите последнее число: ")

if a > b :
    min = b
else:
     min = a

if min > c :
     min = c

if min > d :
     min = d

print( min,"самое маленькое число")