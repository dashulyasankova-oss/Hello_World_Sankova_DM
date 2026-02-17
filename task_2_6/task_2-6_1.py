don = input("Введите фенотип группы крови донора(I, II, III, IV): ").strip().upper()
rec = input("Введите фенотип группы крови реципиента(I, II, III, IV): ").strip().upper()
if don == rec or don=="I":
    print("Переливание возможно!")
else:
    print("Переливание невозмoжно")
