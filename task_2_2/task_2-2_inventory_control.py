# название питательной среды, концентрацию агара (%) и температуру стерилизации.
envir = input()
agar_concent = int(input())
ster_temp = int(input())
with open("C:/Users/User/Desktop/sankova_dm/projects_2/task_2_3/recipe.txt", "w", encoding="utf-8") as recipe:
    recipe.write(f"Введите название питательной среды: {envir}\n")
    recipe.write(f"Введите концентрацию агара (%): {agar_concent}\n")
    recipe.write( f"Введите температуру стерилизации (°C): {ster_temp}\n\n")
    recipe.write("Файл 'recipe.txt' успешно сформирован!\n")
