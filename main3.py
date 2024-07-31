import time
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Настройка Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Функция для парсинга цен на диваны с сайта divan.ru
def parse_prices(url):
    driver.get(url)
    time.sleep(5)  # Ждем загрузки страницы

    prices = []
    while True:
        items = driver.find_elements(By.CLASS_NAME, 'product-price__current')
        for item in items:
            price_text = item.text
            price = int(price_text.replace('₽', '').replace(' ', ''))
            prices.append(price)

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a.pagination-next')
            next_button.click()
            time.sleep(5)  # Ждем загрузки следующей страницы
        except Exception as e:
            print(f"Ошибка: {e}")
            break

    return prices

# URL сайта divan.ru
url = 'https://www.divan.ru/category/divany'

# Парсинг цен на диваны
prices = parse_prices(url)

# Закрытие драйвера
driver.quit()

# Создание DataFrame из полученных данных
df = pd.DataFrame(prices, columns=['Price'])

# Сохранение данных в CSV файл
df.to_csv('divan_prices.csv', index=False)

# Нахождение средней цены
average_price = df['Price'].mean()
print(f'Средняя цена на диваны: {average_price:.2f} ₽')

# Построение гистограммы цен на диваны
plt.figure(figsize=(10, 6))
plt.hist(df['Price'], bins=30, edgecolor='black')
plt.title('Гистограмма цен на диваны')
plt.xlabel('Цена (₽)')
plt.ylabel('Частота')
plt.grid(True)
plt.show()
