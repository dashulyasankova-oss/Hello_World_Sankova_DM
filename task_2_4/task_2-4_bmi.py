num = int(input("Введите общее количество произведенных капсул:"))
density = int(input("Введите количество капсул в одной упаковке:"))
full_boxes = num//density
leftovers = num % density
print("\n--- Отчет фасовочного цеха ---")
print(f"Полных упаковок:\t{full_boxes}\nОстаток капсул:\t{leftovers}")
