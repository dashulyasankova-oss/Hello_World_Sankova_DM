def process_samples(records):
    """
    Обрабатывает пробы: конвертирует value в число и добавляет quality.

    Параметры:
        records: список словарей [{"id": "P1", "value": "7.5"}, ...]

    Возвращает:
        (список_обработанных, список_ошибок)
    """
    processed = []
    errors = []

    for record in records:
        sample_id = record.get("id", "unknown")
        value_str = record.get("value", "")

        try:
            # Пробуем преобразовать в число
            value = float(value_str)

            # Определяем качество
            if value < 5:
                quality = "low"
            elif 5 <= value <= 10:
                quality = "normal"
            else:
                quality = "high"

            # Сохраняем хорошую пробу
            processed.append({
                "id": sample_id,
                "value": value,
                "quality": quality
            })

        except ValueError:
            # Ошибка преобразования
            errors.append(f"Sample {sample_id}: не удалось преобразовать '{value_str}' в число")

    return processed, errors


# ========== ПРИМЕР ==========

# Входные данные
test_data = [
    {"id": "P001", "value": "7.5"},
    {"id": "P002", "value": "3.2"},
    {"id": "P003", "value": "ошибка"},
    {"id": "P004", "value": "12.8"},
    {"id": "P005", "value": "5.0"},
]

# Обрабатываем
good, bad = process_samples(test_data)

# Выводим результаты
print("✅ Хорошие пробы:")
for sample in good:
    print(f"   {sample}")

print(f"\n❌ Ошибки ({len(bad)}):")
for error in bad:
    print(f"   {error}")