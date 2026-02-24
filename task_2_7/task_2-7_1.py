samples = ["seq1", "seq2", "seq3", "seq4"]

sample_date = "2026-03-15"

print("Обработка образцов:")
print("-" * 40)
for sample_id in samples:
    file_name = f"{sample_id}_{sample_date}.fasta"
    print(f"Создан файл: {file_name}")

print("-" * 40)
print(f"Все файлы даты {sample_date} успешно обработаны!")