import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
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

# Функция для рекурсивного обхода сайта
def crawl_site(url, visited_urls, file):
    # Проверяем, если мы уже посещали эту ссылку
    if url in visited_urls:
        print(f"Ссылка уже обработана: {url}")
        return
    
    print(f"Проникаем в {url}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Сначала парсим данные текущей страницы
    udc_data = parse_udc_table(url)
    
    # Записываем данные в файл
    for code, description in udc_data:
        file.write(f"{code}: {description}\n")
    file.flush()  # Сбрасываем данные в файл
    
    # Получаем все ссылки на текущей странице
    links = soup.find_all('a', href=True)
    sub_category_links = [
        urljoin(url, link['href']) 
        for link in links
        if link['href'].endswith('.html')  # Только ссылки на HTML
        and not link['href'].startswith('../index')
        and not link['href'].startswith('about')  # Исключаем index
        and not link['href'].startswith('../dc')  # Исключаем dc
        and "вверх" not in link.text.lower()  # Исключаем ссылки с текстом "вверх"
    ]
    
    # Отмечаем текущий URL как посещённый
    visited_urls.add(url)
    
    # Если есть подкатегории, обходим их
    if sub_category_links:
        print(f"Найдены подкатегории на {url}. Продолжаем обход...")
        for link in sub_category_links:
            crawl_site(link, visited_urls, file)
    else:
        print(f"Ссылок для перехода дальше на {url} нет.")

# Начальная ссылка
base_url = "https://teacode.com/online/udc/"

# Открываем файл для записи данных
with open('udc_data.txt', 'w', encoding='utf-8') as file:
    # Запускаем рекурсивный обход с главной страницы
    visited_urls = set()
    crawl_site(base_url, visited_urls, file)

print("Парсинг завершен, данные сохранены в 'udc_data.txt'.")
