import psycopg2
import sys

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="UBook_diplome",
    user="postgres",
    password="123",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Открываем файл для чтения
with open('udc_data.txt', 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

# Фильтруем строки, удаляя те, где последняя часть после последнего ':' пуста
valid_lines = [
    line for line in lines
    if len(line.rsplit(':', 1)) == 2 and line.rsplit(':', 1)[1].strip() != ''
]

# Перезаписываем файл отфильтрованными строками
with open('udc_data.txt', 'w', encoding='utf-8') as output_file:
    output_file.writelines(valid_lines)

print("Файл успешно обработан: строки с пустым значением после последнего ':' удалены.")

# Открываем отфильтрованный файл и обрабатываем его
with open('udc_data.txt', 'r', encoding='utf-8') as file:
    for line in file:
        try:
            # Разделение строки по двоеточию
            udc_id, udc_name = line.strip().split(':', 1)

            # Выполняем вставку, игнорируя дубликаты
            cursor.execute(
                """
                INSERT INTO UDC (udc_id, udc_name)
                VALUES (%s, %s)
                ON CONFLICT (udc_id) DO NOTHING
                """,
                (udc_id.strip(), udc_name.strip())  # Удаляем лишние пробелы
            )

        except psycopg2.errors.StringDataRightTruncation as e:
            # Выводим строку, которая вызывает ошибку
            print(f"Ошибка при вставке строки: {line.strip()}")
            print(f"Ошибка: {e}")
            # Завершаем выполнение программы
            sys.exit(1)
        except Exception as e:
            # Обрабатываем другие возможные ошибки
            print(f"Неизвестная ошибка при обработке строки: {line.strip()}")
            print(f"Ошибка: {e}")
            # Завершаем выполнение программы
            sys.exit(1)

# Подтверждение изменений и закрытие соединения
conn.commit()
cursor.close()
conn.close()
