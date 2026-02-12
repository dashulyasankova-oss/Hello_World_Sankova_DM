reactive_name = input()
reactive_quant = int(input())
notif = f"Реактив {reactive_name} поступил на склад в количестве {reactive_quant} шт.."
f = open("notification.txt", "w", encoding="utf-8")
print(notif, file=f)
f.close()
