import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse
from pathlib import Path

def create_time_series(file_path, date_col, value_col):
    """
    Читает временной ряд из файла csv
    
    Args:
        file_path (str): путь к файлу с данными
        date_col (str): название столбца с датами
        value_col (str): название столбца со значениями
    Returns:
        pd.DataFrame: DataFrame с колонками 'date' и 'value'
    Raises:
        FileNotFoundError: если файл не существует
        ValueError: если не поддерживается формат файла
        KeyError: если отсутствуют необходимые колонки
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден")

    file_ext = os.path.splitext(file_path)[1]

    try: 
        if file_ext == '.csv':
            df = pd.read_csv(file_path, parse_dates=[date_col])
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {file_ext}")
        
        if date_col not in df.columns:
            raise KeyError(f"Колонка {date_col}  не найдена в файле")
        if value_col not in df.columns:
            raise KeyError(f"Колонка {value_col} не найдена в файле")
        df[date_col] = pd.to_datetime(df[date_col])

        return df
    except Exception as e:
        raise Exception(f"Ошибка чтения файла: {str(e)}")


def calculation_moving_average(df, window, value_col, new_col=None):
    """
    Считает скользящее среднее
    
    Args:
        df (pd.DataFrame): DataFrame
        window (int): размер окна
        value_col (str): название столбца с значениями
        new_col (str): название для нового столбца
    Returns:
        pd.DataFrame: DataFrame с новой колонкой
    Raises:
        TypeError: если значения не числовые
    """
    try:
        numeric_values = pd.to_numeric(df[value_col], errors='raise')
    except ValueError as e:
        raise TypeError(f"Столбец 'value' содержит нечисловые значения: {e}")

    df[new_col] = df[value_col].rolling(window=window, min_periods=1).mean()

    return df

def build_graphic(df, output_file, format_file, date_col, value_col, new_col):
    """
    Строит и сохраняет график временного ряда и скользящего среднего (в формате jpg, pdf, png с названием moving_average)
    
    Args:
        df (pd.DataFrame): DataFrame с данными
        output_file (str): директория для сохранения файла
        format_file (str): формат файла
        date_col (str): название столбца с датами
        value_col (str): название столбца с исходными значениями
        new_col (str): название нового столбца
    Returns:
        plt.Figure: объект фигуры matplotlib
    """
    fig = plt.figure(figsize=(12,6))
    plt.plot(df[date_col], df[value_col], label='Исходные данные', linewidth=2)
    plt.plot(df[date_col], df[new_col], label=new_col, linewidth=2)

    plt.title('Временной ряд и скользящее среднее')
    plt.xlabel(date_col)
    plt.ylabel(value_col)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)

    # создаём полный путь к файлу
    output_path = Path(output_file) / f"moving_average.{format_file}"

    # убедимся, что директория существует
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # сохраняем график
    plt.savefig(output_path, format=format_file, dpi=300)
    plt.show()

    return fig

    

def main():
    #  создание временного ряда
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Путь к входному файлу')
    parser.add_argument('-o', '--output', default='output', help='Директория для результатов')
    parser.add_argument('-w', '--window', type=int, default=3, help='Размер окна для скользящего среднего (по умолчанию: 3)')
    parser.add_argument('--format', default='png', choices=['png', 'pdf', 'jpg'], help='Формат графика')
    parser.add_argument('--date-col', default='date', help='Название столбца с датами (по умолчанию: date)')
    parser.add_argument('--value-col', default='value', help='Название столбца с числовыми значениями (по умолчанию: value)')
    parser.add_argument('--new-col', help='Название для нового столбца')
    args = parser.parse_args()

    print(args.output)
    df = create_time_series(args.input_file, args.date_col, args.value_col)
    #  вычисление скользящего среднего
    res = calculation_moving_average(df, args.window, args.value_col, args.new_col)
    #  построение и сохранение графика
    fig = build_graphic(res, args.output, args.format, args.date_col, args.value_col, args.new_col)
    

if __name__ == "__main__":
    main()

