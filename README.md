# Формирование прогнозной модели оттока действующих клиентов

# Прогноз модели основывается:
1) На данных о том в какой месяц клиент выполняет активность 
Учитывает объем перевозок, провозную плату в какое время перевозят груз
Зависимость: 78%

2) На позитивных обращениях
Учитывает взаимодействие клиента с РЖД за промежуток времени
Зависимость: 20%

3) На добросоветности клиента
Учитывает данные о платежах по счетам и финансовые риски
Зависимость: 98%

## Первоначальный анализ зависимостей параметров (за 6 последних месяцев) - маленькая зависимость
![Models](https://github.com/Ghost-Name/Hackathon_PVD/blob/PNG/PNG/analysis_V1.png)

## Конечный анализ зависимостей вычесленных + первоначальных параметров (за 12 последних месяцев) - средняя зависимость
![Models](https://github.com/Ghost-Name/Hackathon_PVD/blob/PNG/PNG/analysis_V2.png)

## Анализ результатов обученных моделей
![Models](https://github.com/Ghost-Name/Hackathon_PVD/blob/PNG/PNG/models.png)

## Преимущества MAE:
* Интуитивность: MAE легко интерпретируется и показывает среднюю ошибку в тех же единицах, что и данные.
* Чувствительность к выбросам: MAE менее чувствительна к выбросам по сравнению с другими метриками, такими  как MSE (Mean Squared Error), поскольку не возводит ошибки в квадрат.

### Gradient Boosting: 15.34

  Оценка: Хорошо (между 10% и 20%)
### Random Forest: 15.33

  Оценка: Хорошо (между 10% и 20%)
### Linear Regression: 13.99

Оценка: Хорошо (между 10% и 20%)

# **Spectral Paladin**

 **Copyright (c) 2024 Gureev Ilya gureev.ilya.nvk@gmail.com**

