# Открываем файл для чтения
with open('udc_data.txt', 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

# Фильтруем строки, удаляя те, которые содержат символ '$'
valid_lines = [line for line in lines if '$=' not in line]

# Перезаписываем файл отфильтрованными строками
with open('udc_data.txt', 'w', encoding='utf-8') as output_file:
    output_file.writelines(valid_lines)

print("Файл успешно обработан: строки с символом '$=' удалены.")
