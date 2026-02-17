value = float(input("Введите нужный объём раствора(мл):"))
mass_salt = float(value*0.009)

with open("C:/Users/User/Desktop/sankova_dm/projects_2/task_2_4/recipe.txt", "w", encoding="utf-8") as end:
    end.write(("ОТЧЕТ ПО ПРИГОТОВЛЕНИЮ:\n-----------------------\n"))
    end.write(f"Общий объем: {value} мл\nМасса соли: {mass_salt:.3f} г\nОбъем воды: {value} мл")
