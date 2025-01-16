import requests
from bs4 import BeautifulSoup

url = "https://teacode.com/online/udc/"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

# Находим таблицу по атрибутам
table = soup.find('table', {'border': '0', 'width': '500', 'cellpadding': '3', 'cellspacing': '2'})

# Извлекаем строки таблицы, пропуская заголовок
table_rows = table.find_all('tr')[1:]  # Пропускаем заголовок

udc_data = []
for row in table_rows:
    columns = row.find_all('td')
    if len(columns) == 3:  # Убедимся, что в строке три столбца
        code = columns[0].text.strip()  # Код УДК
        description = columns[1].text.strip()  # Описание
        if code.strip() == "":  # Пропускаем строку с итогами
            continue
        # Убираем все лишние переводы строк в описании
        description = " ".join(description.splitlines())
        udc_data.append((code, description))

# Сохраняем данные в файл
with open('udc_data.txt', 'w', encoding='utf-8') as file:
    for code, description in udc_data:
        file.write(f"{code}: {description}\n")
