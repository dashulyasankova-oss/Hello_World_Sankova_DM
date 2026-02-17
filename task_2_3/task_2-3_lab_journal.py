name = input()
date = input()
exp = input() #experiment
conc = input() #conclusion

# я придумала супер-систему (нет), чтобы табличка была ровная и красивая, 
# работает с помощью счета длины строк
# _p - значит processed
# _f - значит final

line = "+--------------------------------------------------+"
line_len = len(line)-1
len_main = len("| ФИО исследователя ") 
# len_main самая длинная среди остальных main, поэтому опираемся на неё

name_p = (f"| ФИО исследователя :" + (name))
name_len = len(name_p)
name_f = ("\n" + (name_p) + " "*(line_len-name_len) + "|")
# считаем сколько символов в выводе и сколько не хватает до конца и вставляем туда палочку

date_main = "| Дата"
date_p = (date_main + " "*(len_main-len(date_main)) + ":" + date)
# выравниваю двоеточия, чтобы все в ряд стояли
date_len = len(date_p)
date_f = ("\n" + (date_p) + " "*(line_len-date_len) + "|")
# вставила палочку в конце

exp_main = "| Эксперимент"
exp_p = (exp_main + " "*(len_main-len(exp_main)) + ":" + exp)
# выравниваю двоеточия, чтобы все в ряд стояли
exp_len = len(exp_p)
exp_f = ("\n" + (exp_p) + " "*(line_len-exp_len) + "|"+ "\n")
# вставила палочку в конце


# c conc'ом сложнее, он очень длинный, я решила его попилить на несколько строк, опираясь на длину рамки
conc_main = ("| Вывод:")
conc_out = (conc_main + " "*(line_len-len(conc_main)) + "|")
# причесала строку вывода
rows = [conc[i:i+(line_len-1)] for i in range(0, len(conc), line_len)]
# попилила на части ввод
conc_p = ("|" + "|\n|".join(rows) + " "*(line_len-(len(conc) % line_len)-1)+ "|")
# причесала строки ввода
conc_f = ("\n" + conc_out + "\n" + conc_p+"\n")

with open("C:/Users/User/Desktop/sankova_dm/projects_2/task_2_3/journal.txt", "w", encoding="utf-8") as end:
    end.write(line)
    end.write("\n| Электронный лабораторный журнал                  |\n")
    end.write(line)
    end.write(name_f)
    end.write(date_f)
    end.write(exp_f)
    end.write(line)
    end.write(conc_f)
    end.write(line)
    
#вывод всей информации в файл