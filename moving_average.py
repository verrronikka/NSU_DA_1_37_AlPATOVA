import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse
from pathlib import Path

def create_time_series(file_path):
    """
    Читает временной ряд из файла csv
    
    Args:
        file_path (str): путь к файлу с данными
        
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
            df = pd.read_csv(file_path, parse_dates=['date'])
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {file_ext}")
        
        if 'date' not in df.columns:
            raise KeyError("Колонка 'date' не найдена в файле")
        if 'value' not in df.columns:
            raise KeyError("Колонка 'value' не найдена в файле")

        return df
    except Exception as e:
        raise Exception(f"Ошибка чтения файла: {str(e)}")


def calculation_moving_average(df, window):
    """
    Считает скользящее среднее
    
    Args:
        df (pd.DataFrame): DataFrame с колонками 'date' и 'value' 

    Returns:
        pd.DataFrame: DataFrame с колонками 'date', 'value', 'SMA'  
    """

    df['SMA'] = df['value'].rolling(window=window, min_periods=1).mean()

    return df

def build_graphic(df, output_file, format_file):
    """
    Строит и сохраняет график временного ряда и скользящего среднего (в формате jpg, pdf, png с названием moving_average)
    
    Args:
        df (pd.DataFrame): DataFrame с колонками 'date', 'value', 'SMA'
        output_dir (str): директория для сохранения файла
        format_file (str): формат файла ('png', 'pdf', 'jpg')

    Returns:
        plt.Figure: объект фигуры matplotlib
    """
    fig = plt.figure(figsize=(12,6))
    plt.plot(df['date'], df['value'], label='Исходные данные', linewidth=2)
    plt.plot(df['date'], df['SMA'], label='Скользящее среднее', linewidth=2)

    plt.title('Скользящее среднее')
    plt.xlabel('Дата')
    plt.ylabel('Значение')
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
    args = parser.parse_args()

    print(args.output)
    df = create_time_series(args.input_file)
    #  вычисление скользящего среднего
    res = calculation_moving_average(df, args.window)
    #  построение графика
    fig = build_graphic(res, args.output, args.format)
    
    return 0

if __name__ == "__main__":
    main()

