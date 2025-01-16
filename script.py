import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Функция для парсинга таблицы с кодами УДК
def parse_udc_table(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Находим таблицу по атрибутам
    table = soup.find('table', {'border': '0', 'width': '500', 'cellpadding': '3', 'cellspacing': '2'})
    
    if not table:
        print(f"Таблица не найдена на странице: {url}")
        return []
    
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
    
    return udc_data

# Начальная ссылка
base_url = "https://teacode.com/online/udc/"

# Получаем начальную страницу
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Парсим таблицу с главной страницы
print(f"Парсинг данных с {base_url}...")
main_page_data = parse_udc_table(base_url)

# Находим все ссылки на подкатегории УДК (исключаем текущую страницу)
links = soup.find_all('a', href=True)

# Создаем полный URL для каждой ссылки
sub_category_links = [urljoin(base_url, link['href']) for link in links if link['href'].startswith('./')]

# Открываем файл для записи данных
with open('udc_data.txt', 'w', encoding='utf-8') as file:
    data_found = False  # Переменная для отслеживания, были ли найдены данные
    # Записываем данные с главной страницы
    if main_page_data:
        data_found = True
        for code, description in main_page_data:
            file.write(f"{code}: {description}\n")
    else:
        print(f"Нет данных для записи на главной странице.")

    # Парсим данные для каждой подкатегории
    for link in sub_category_links:
        print(f"Парсинг данных с {link}...")
        # Парсим таблицу с кодами УДК на текущей странице
        udc_data = parse_udc_table(link)
        
        # Проверяем, что данные были получены
        if udc_data:
            data_found = True
            # Записываем данные в файл
            for code, description in udc_data:
                file.write(f"{code}: {description}\n")
        else:
            print(f"Нет данных для записи на странице: {link}")

    if not data_found:
        print("Данные не были найдены на страницах.")

print("Парсинг завершен, данные сохранены в 'udc_data.txt'.")
