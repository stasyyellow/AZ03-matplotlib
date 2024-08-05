import time
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    driver.get(url)  # Переход на заданный URL (divan.ru)
    time.sleep(5)  # Ждем загрузки страницы

    prices = []
    while True:
        items = driver.find_elements(By.CLASS_NAME, 'ui-LD-ZU.KIkOH')  # Получаем элементы с классом 'product-price__current'
        for item in items:
            price_text = item.text  # Извлекаем текст цены
            price_text = price_text.replace('руб', '').replace(' ', '').replace('.', '')  # Преобразуем цену в числовой формат
            try:
                price = int(price_text)
                prices.append(price)
            except ValueError:
                print(f"Невозможно преобразовать в int: {price_text}")

        try:
            # Используем явные ожидания для нахождения кнопки "Далее"
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.wDTtf.cursor-default-hover'))
            )
            next_button.click()  # Кликаем по кнопке
            time.sleep(5)  # Ждем загрузки следующей страницы
        except Exception as e:
            print(f"Ошибка: {e}")  # Выводим ошибку, если переход на следующую страницу не удался
            break  # Прекращаем цикл, если нет кнопки "Далее"

    return prices

# URL сайта divan.ru
url = 'https://www.divan.ru/category/divany-i-kresla'

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
   
#ui-jDl24 cursor-default-hover