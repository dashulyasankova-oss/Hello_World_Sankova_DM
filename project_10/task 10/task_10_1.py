pickles = [
    {"sku": "A1", "category": "flour", "expected": 100, "actual": 95},
    {"sku": "B2", "category": "sugar", "expected": 50, "actual": 50},
    {"sku": "C3", "category": "enzyme", "expected": 10, "actual": 12},
]

differ = []
dict_cat = {}

for cucumba in pickles:
    sku = cucumba["sku"]
    expected = cucumba["expected"]
    actual = cucumba["actual"]
    category = cucumba["category"]

    if actual != expected:
        raz = actual - expected
        differ.append((sku, raz))
        if raz < 0:
            print("Расхождения: недостает", cucumba["category"], "меньше ожидaемого на", abs(raz))
        elif raz > 0:
            print("Расхождения: избыток", cucumba["category"], "больше ожидaемого на", abs(raz))

    if category not in dict_cat:
        dict_cat[category] = []
    dict_cat[category].append(sku)
print(f"Категории:{dict_cat}")