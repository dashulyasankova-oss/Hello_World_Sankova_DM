import psycopg2
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt  # Закомментировано, т.к. не используется

matplotlib.rcParams['font.family'] = 'DejaVu Sans'

connection = None  # ← Инициализируем переменную заранее

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="example",
        database="testdb"
    )
    print("✓ Подключение установлено")

    df_courses = pd.read_sql("""
        SELECT
            c.course_name AS course,
            ROUND(AVG(e.grade)::numeric, 2) AS avg_grade,
            COUNT(e.enrollment_id) AS total_enrollments
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        GROUP BY c.course_name
        ORDER BY avg_grade DESC
    """, connection)

    df_years = pd.read_sql("""
        SELECT
            enrollment_year AS year,
            COUNT(student_id) AS students
        FROM students
        GROUP BY enrollment_year
        ORDER BY enrollment_year
    """, connection)

    df_all = pd.read_sql("SELECT grade FROM enrollments", connection)

    df_missing = pd.read_sql("""
        SELECT
            s.first_name || ' ' || s.last_name AS student,
            s.enrollment_year
        FROM students s
        LEFT JOIN enrollments e ON s.student_id = e.student_id
        WHERE e.enrollment_id IS NULL
        ORDER BY s.enrollment_year, s.last_name
    """, connection)

    print(f"Курсов в выборке:           {len(df_courses)}")
    print(f"Всего записей об оценках:   {len(df_all)}")
    print(f"Студентов без оценок (ан.): {len(df_missing)}")

except psycopg2.Error as error:  # ← Сужаем тип ошибки
    print(f"Ошибка подключения: {error}")
    raise SystemExit

finally:
    if connection:  # ← Проверяем, что connection существует
        connection.close()
        print("✓ Соединение закрыто\n")


#6. Построение графиков!!!!


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(
    2, 2,
    figsize=(14, 10)   # ширина × высота в дюймах
)
fig.suptitle("Анализ учебной базы данных", fontsize=16, fontweight="bold", y=1.01)



#6.1. Средний балл по курсам (столбчатая диаграмма)


df_courses["short_name"] = df_courses["course"].str[:12]
bars1 = ax1.bar(
    df_courses["short_name"],     # Ось X — названия курсов
    df_courses["avg_grade"],      # Ось Y — средний балл
    color="#4a90d9",              # Синий цвет столбцов
    edgecolor="white",            # Белая обводка для разделения столбцов
    width=0.6
)

# Задаём порог нормы (можно менять)
NORM_THRESHOLD = 3.8

# Определяем цвета: красный если ниже нормы (3.8), иначе синий
colors = [
    "red" if grade < NORM_THRESHOLD else "#4a90d9"
    for grade in df_courses["avg_grade"]
]

bars1 = ax1.bar(
    df_courses["short_name"],     # Ось X — названия курсов
    df_courses["avg_grade"],      # Ось Y — средний балл
    color=colors,                 # ← Цвета зависят от нормы
    edgecolor="white",
    width=0.6
)

# Подпись значения НАД каждым столбцом

for bar, val in zip(bars1, df_courses["avg_grade"]):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,  # Центр столбца по X
        bar.get_height() + 0.05,            # Чуть выше столбца по Y
        f"{val:.2f}",                       # Текст: число с 2 знаками
        ha="center", fontsize=9
    )

# Горизонтальная линия — среднее по всем курсам
mean_grade = df_courses["avg_grade"].mean()
ax1.axhline(mean_grade, color="crimson", linestyle="--", linewidth=1.2,
            label=f"Среднее: {mean_grade:.2f}")


ax1.set_ylim(0, 5.5)              # Диапазон оси Y (оценки от 0 до 5)
ax1.set_ylabel("Средний балл")
ax1.set_title("Средний балл\nпо курсам", fontweight="bold", pad=8)
ax1.set_xticks(range(len(df_courses)))
ax1.set_xticklabels(df_courses["short_name"], rotation=40, ha="right", fontsize=8)
ax1.legend(fontsize=8)


#6.2. Количество сдач по курсам


bars2 = ax2.bar(

    df_courses["short_name"],

    df_courses["total_enrollments"],

    color="#2ecc71",    # Зелёный цвет

    edgecolor="white",

    width=0.6

)



# Подпись числа над каждым столбцом

for bar, val in zip(bars2, df_courses["total_enrollments"]):

    ax2.text(

        bar.get_x() + bar.get_width() / 2,

        bar.get_height() + 0.1,

        str(val),

        ha="center", fontsize=9

    )



ax2.set_ylim(0, max(df_courses["total_enrollments"]) + 2.5)

ax2.set_ylabel("Количество сдач")

ax2.set_title("Количество сдач\nпо курсам", fontweight="bold", pad=8)

ax2.set_xticks(range(len(df_courses)))

ax2.set_xticklabels(df_courses["short_name"], rotation=40, ha="right", fontsize=8)


#6.3. Студенты по году поступления (круговая диаграмма)


pie_colors = ["#7b68ee", "#4a90d9", "#2ecc71"]
# Подписи для легенды: "2023 (10 чел.)"
pie_labels = [f"{row.year} ({row.students} чел.)" for _, row in df_years.iterrows()]

wedges, texts, autotexts = ax3.pie(
    df_years["students"],           # Значения секторов
    labels=None,                    # Подписи выведем в легенду, не на сектора
    autopct="%1.0f%%",              # Показывать процент внутри сектора
    colors=pie_colors,
    startangle=90,                  # Начинаем с "12 часов" — интуитивно привычно
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    pctdistance=0.7                 # Расстояние подписи % от центра (0=центр, 1=край)
)

# Делаем подписи процентов жирными
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight("bold")

ax3.set_title("Студенты\nпо году набора", fontweight="bold", pad=8)

# Легеyда с числами под диаграммой
ax3.legend(
    wedges, pie_labels,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.22),   # Координаты легенды относительно графика
    fontsize=8,
    frameon=False                  # Без рамки вокруг легенды
)


#6.4. Распределение оценок (гистограмма + аннотации)


# Считаем, сколько раз встречается каждая оценка
grade_counts = df_all["grade"].value_counts().sort_index()

bars4 = ax4.bar(
    grade_counts.index,      # Оценки: 2, 3, 4, 5
    grade_counts.values,     # Количество записей
    color="#f0ad4e",         # Оранжевый
    edgecolor="white",
    width=0.5               # Узкие столбцы — наглядно, что шкала дискретная
)

# Подписи над столбцами: "12 (24%)"
for bar, (grade, cnt) in zip(bars4, grade_counts.items()):
    ax4.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        f"{cnt} ({cnt / len(df_all) * 100:.0f}%)",   # Число и процент
        ha="center", fontsize=9
    )

# Вертикальная линия — медиана
median_grade = df_all["grade"].median()
ax4.axvline(median_grade, color="crimson", linestyle="--",
            linewidth=1.5, label=f"Медиана: {median_grade}")

# Аннотация-стрелка на аномалию: оценка «2» — единственная ниже 3
if 2 in grade_counts.index:
    ax4.annotate(
        f"Аномалия:\n{grade_counts[2]} оценки «2»",
        xy=(2, grade_counts[2]),          # Куда указывает стрелка (на столбец)
        xytext=(2.4, grade_counts[2] + 4),# Откуда начинается текст
        arrowprops={"arrowstyle": "->", "color": "crimson"},
        fontsize=8, color="crimson"
    )

ax4.set_xticks([2, 3, 4, 5])
ax4.set_xlabel("Оценка")
ax4.set_ylabel("Количество записей")
ax4.set_title("Распределение оценок", fontweight="bold", pad=8)
ax4.legend(fontsize=8)

# Текстовый блок со статистикой прямо на графике
stats_text = (
    f"Всего оценок: {len(df_all)}\n"
    f"Среднее: {df_all['grade'].mean():.2f}\n"
    f"Ст. откл.: {df_all['grade'].std():.2f}"
)
ax4.text(
    0.97, 0.95,           # Координаты в долях осей (0–1), правый верхний угол
    stats_text,
    transform=ax4.transAxes,   # Координаты относительно области графика, не данных
    va="top", ha="right", fontsize=8,
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "lightyellow",
          "edgecolor": "lightgray", "alpha": 0.8}
)


#6.5. Подпись об аномалии под всей фигурой


fig.text(
    0.5, -0.03,    # Центр по X, чуть ниже фигуры по Y
    f"⚠ Аномалия: {len(df_missing)} из {df_years['students'].sum()} студентов "
    "не имеют ни одной записи об успеваемости (отсутствует в таблице enrollments)",
    ha="center", fontsize=9, color="#8b0000",
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "#fff3f3", "edgecolor": "#d9534f"}
)


#6.6. Сохранение


plt.tight_layout()   # Автоматически убирает перекрытия между графиками

OUTPUT_FILE = "student_charts.png"
plt.savefig(
    OUTPUT_FILE,
    bbox_inches="tight",   # Обрезает пустые поля вокруг фигуры
    dpi=150                # Разрешение: 150 точек на дюйм (хорошее качество)
)
print(f"✓ График сохранён: {OUTPUT_FILE}")
plt.show()   # Показывает окно с графиком (если запускаете интерактивно)