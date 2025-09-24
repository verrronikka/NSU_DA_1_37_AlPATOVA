# About
Код задачи moving_average выполняет следующее:
  - Создание временного ряда
  - Вычисление скользящего среднего
  - Построение и сохранение графика 

## Структура кода

- `create_time_series(file_path, date_col, value_col)` — чтение 
- `calculation_moving_average(df, window, value_col, new_col=None)` — вычисление скользящего среднего
- `build_graphic(df, output_file, format_file, date_col, value_col, new_col)` — построение и сохранение графика
- `main()` — основная функция
## Зависимости
  pip install pandas matplotlib
## Запуск
  python moving_average.py test.csv
## Вывод программы
<img width="2256" height="1364" alt="image" src="https://github.com/user-attachments/assets/445ecc09-e352-4f1e-8c2f-87a88d66ff34" />
