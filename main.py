import numpy as np
import matplotlib.pyplot as plt

# Параметры нормального распределения
mean = 0  # Среднее значение
std_dev = 1  # Стандартное отклонение
num_samples = 1000  # Количество образцов

# Генерация случайных чисел, распределенных по нормальному распределению
data = np.random.normal(mean, std_dev, num_samples)

# Построение гистограммы
plt.figure(figsize=(10, 6))
plt.hist(data, bins=30, edgecolor='black')
plt.title('Гистограмма нормального распределения')
plt.xlabel('Значение')
plt.ylabel('Частота')
plt.grid(True)
plt.show()

# Генерация двух наборов случайных данных
x = np.random.rand(100)  # массив из 100 случайных чисел для оси x
y = np.random.rand(100)  # массив из 100 случайных чисел для оси y

# Построение диаграммы рассеяния
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', alpha=0.5)
plt.title('Диаграмма рассеяния для случайных данных')
plt.xlabel('Значения X')
plt.ylabel('Значения Y')
plt.grid(True)
plt.show()
