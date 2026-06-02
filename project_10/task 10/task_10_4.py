def process_samples(records):

    processed = [] #списки хороших и плохих
    errors = []

    for record in records:
        sample_id = record.get("id", "unknown") #для каждой строки достаем данные для обработки
        value_str = record.get("value", "")

        try:
            value = float(value_str) #пробуем сделать float
            if value < 5: #присваиваем качество
                quality = "low"
            elif 5 <= value <= 10:
                quality = "normal"
            else:
                quality = "high"

            processed.append({ #аккуратненько записываем хорошие пробы
                "id": sample_id,
                "value": value,
                "quality": quality
            })

        except ValueError: #если цыфорка не поплыла
            errors.append(f"Sample {sample_id}: не удалось преобразовать '{value_str}' в число") #записали плохие пробы

    return processed, errors #запомнили в таком порядке


test_data = [
    {"id": "P001", "value": "7.5"},
    {"id": "P002", "value": "3.2"},
    {"id": "P003", "value": "ошибка"},
    {"id": "P004", "value": "12.8"},
    {"id": "P005", "value": "5.0"},
]

good, bad = process_samples(test_data) #обработали и в том же порядке записали

print("Хорошие пробы:")
for sample in good:
    print(f"   {sample}")

print(f"\nОшибки ({len(bad)}):")
for error in bad:
    print(f"   {error}")