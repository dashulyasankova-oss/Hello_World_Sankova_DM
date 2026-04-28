n = int(input("Введите колчиество чисел: "))

max_num = None

for i in range(n):
    num = int(input(f"Введите числа {i + 1}: "))
    
    if max_num is None or num > max_num:
        max_num = num

print("Самое большое число", max_num)