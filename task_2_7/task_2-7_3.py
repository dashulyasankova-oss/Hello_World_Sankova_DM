sequences = ["ATATACGCGTA", "CTTCGGNGGA"]

print("=" * 50)
print("Анализ последовательности ДНК:")
print("=" * 50 + "\n")

for i, seq in enumerate(sequences, 1):
    print(f"Последовательность {i}:")
    print(f"\tЦеликом: {seq}")
    print(f"\tПострочно:")

    for j, nucleotide in enumerate(seq, 1):
        print(f"    {j:2d}. {nucleotide}")
    
    print("-" * 40)
print("\nЦикл выполнен!")