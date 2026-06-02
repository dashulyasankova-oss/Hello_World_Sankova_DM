import json


def analyze_process_logs(jsonl_path, report_path):
    """
    Анализирует JSONL файл с технологическими логами.

    Параметры:
        jsonl_path (str): путь к входному JSONL файлу
        report_path (str): путь для сохранения отчёта

    Возвращает:
        dict: словарь с количеством событий по уровням
    """
    level_counts = {}
    total = 0

    # Открываем и читаем файл
    with open(jsonl_path, 'r', encoding='utf-8') as file:
        # Читаем построчно
        for line in file:
            # Удаляем пробелы в начале и конце строки
            line = line.strip()

            # Пропускаем пустые строки
            if not line:
                continue

            # Преобразуем JSON строку в словарь
            try:
                log_entry = json.loads(line)
            except json.JSONDecodeError:
                print(f"Ошибка: неверный формат JSON в строке: {line[:50]}")
                continue

            # Получаем уровень логирования
            level = log_entry.get('level', 'UNKNOWN')

            # Увеличиваем счётчик для этого уровня
            if level not in level_counts:
                level_counts[level] = 0
            level_counts[level] += 1
            total += 1

    # Формируем отчёт
    report_lines = [
        "Process Log Report",
        "=================="
    ]

    # Добавляем строки для каждого уровня
    for level, count in sorted(level_counts.items()):
        report_lines.append(f"{level}: {count}")

    # Добавляем итоговую строку
    report_lines.append(f"Total: {total}")

    # Записываем отчёт в файл
    with open(report_path, 'w', encoding='utf-8') as report_file:
        report_file.write('\n'.join(report_lines))

    return level_counts

# Пример использования:
# result = analyze_process_logs('process_logs.jsonl', 'report.txt')
# print(result)
