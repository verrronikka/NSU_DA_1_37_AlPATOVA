import pandas as pd
import matplotlib.pyplot as plt
import os


def create_time_series(file_path):
    """
    Читает временной ряд из файла csv
    
    Args:
        file_path (str): путь к файлу с данными
        
    Returns:
        pd.DataFrame: DataFrame с колонками 'date' и 'value'
        
    Raises:
        ValueError: если не поддерживается формат файла
    """


    file_ext = os.path.splitext(file_path)[1]
    
    if file_ext == '.csv':
        df = pd.read_csv(file_path, parse_dates=['date'])
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {file_ext}")
    
    return df


def calculation_moving_average(df):
    """
    Считает скользящее среднее
    
    Args:
        df (pd.DataFrame): DataFrame с колонками 'date' и 'value' 

    Returns:
        pd.DataFrame: DataFrame с колонками 'date', 'value', 'SMA'  
    """

    df['SMA'] = df['value'].rolling(window=3).mean()

    return df

def build_graphic(df):
    """
    Строит график временного ряда и скользящего среднего
    
    Args:
        df (pd.DataFrame): DataFrame с колонками 'date', 'value', 'SMA'
    """
    plt.figure(figsize=(12,6))
    plt.plot(df['date'], df['value'], label='Исходные данные', linewidth=2)
    plt.plot(df['date'], df['SMA'], label='Скользящее среднее', linewidth=2)

    plt.title('Скользящее среднее')
    plt.xlabel('Дата')
    plt.ylabel('Значение')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.show()
    

def main():
    #  создание временного ряда
    df = create_time_series('test.csv')
    #  вычисление скользящего среднего
    res = calculation_moving_average(df)
    #  построение графика
    build_graphic(res)
    
    return 0

if __name__ == "__main__":
    main()

