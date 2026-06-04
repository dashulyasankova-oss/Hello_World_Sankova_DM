import psycopg2
import pandas as pd
import matplotlib
# import matplotlib.pyplot as plt  # Закомментировано, т.к. не используется

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