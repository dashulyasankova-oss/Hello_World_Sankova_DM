temp = float(input("Какая температура листа сейчас? (Вводите значение без '°C'): "))

if float("-inf") < temp < 5:

    print("Ho, you visiting Santa on da North Pole?")

elif 5 <= temp <= 25:

    print("Оптимальная температура для растений с C3-метаболизмом")

elif 25 < temp <= 35:

    print("Хорошо для растений с C4-метаболизмом")

else:

    print("It's hot as hell! Cool down, bro.")

