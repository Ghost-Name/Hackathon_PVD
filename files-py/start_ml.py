import os
import pandas as pd

def find_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def filter_data(query_params):
    filename = 'test.xlsx'
    search_path = '.'  # Путь к директории, в которой начнем поиск. '.' - это текущая директория.

    # Поиск файла
    file_path = find_file(filename, search_path)
    
    if file_path is None:
        raise FileNotFoundError(f"Файл '{filename}' не найден в '{search_path}'.")

    # Загрузка данных из Excel файла
    data = pd.read_excel(file_path)

    # Извлечение параметров фильтрации
    filters = {
        'isMSP': query_params.get('isMSP'),
        'companySize': query_params.get('companySize'),
        'cityActual': query_params.get('cityActual'),
        'shipper': query_params.get('shipper'),
        'consignee': query_params.get('consignee')
    }

    # Инициализация отфильтрованных данных
    filtered_data = data

    # Применение фильтров только если они не пустые или NaN
    if pd.notna(filters['isMSP']) and filters['isMSP'] != '':
        filtered_data = filtered_data[filtered_data['Находится в реестре МСП'] == filters['isMSP']]
    if pd.notna(filters['companySize']) and filters['companySize'] != '':
        filtered_data = filtered_data[filtered_data['Размер компании.Наименование'] == filters['companySize']]
    if pd.notna(filters['cityActual']) and filters['cityActual'] != '':
        filtered_data = filtered_data[filtered_data['Город фактический'] == filters['cityActual']]
    if pd.notna(filters['shipper']) and filters['shipper'] != '':
        filtered_data = filtered_data[filtered_data['Грузоотправитель'] == filters['shipper']]
    if pd.notna(filters['consignee']) and filters['consignee'] != '':
        filtered_data = filtered_data[filtered_data['Грузополучатель'] == filters['consignee']]

    # Ограничение на вывод 50 записей
    result = filtered_data[['ID', 'leavingChance']].head(50).to_dict(orient='records')

    return result

# Пример использования:
query_params = {
    'isMSP': 'Нет',
    'companySize': 'Крупный бизнес',
    'cityActual': '',
    'shipper': 'Да',
    'consignee': 'Да'
}

try:
    output = filter_data(query_params)
    print(output)
except FileNotFoundError as e:
    print(e)
