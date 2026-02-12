# имя оператора и текущее значение датчика давления.
name = input()
val_press = input()

with open("C:/Users/User/Desktop/sankova_dm/projects_2/task_2_3/sensor.txt", "w", encoding="utf-8") as log:
    log.write(f"Введите имя оператора: {name}\n")
    log.write( f"Введите текущее значение давления (Па): {val_press}\n\n")
    log.write("Файл 'sensor.txt' успешно сформирован!\n")