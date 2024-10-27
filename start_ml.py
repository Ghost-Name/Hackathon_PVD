import pandas as pd

# file_path - r'uploaded_files\test.xlsx'
def filter_data(file_path, query_params):

    data = pd.read_excel(file_path)

    # Получаем параметры фильтрации
    filters = {
        'isMSP': query_params.get('isMSP'),
        'companySize': query_params.get('companySize'),
        'cityActual': query_params.get('cityActual'),
        'shipper': query_params.get('shipper'),
        'consignee': query_params.get('consignee')
    }

    # Применяем фильтры
    filtered_data = data

    # И применяем фильтры только если они не NaN
    if pd.notna(filters['isMSP']):
        filtered_data = filtered_data[filtered_data['Находится в реестре МСП'] == filters['isMSP']]
    if pd.notna(filters['companySize']):
        filtered_data = filtered_data[filtered_data['Размер компании.Наименование'] == filters['companySize']]
    if pd.notna(filters['cityActual']):
        filtered_data = filtered_data[filtered_data['Город фактический'] == filters['cityActual']]
    if pd.notna(filters['shipper']):
        filtered_data = filtered_data[filtered_data['Грузоотправитель'] == filters['shipper']]
    if pd.notna(filters['consignee']):
        filtered_data = filtered_data[filtered_data['Грузополучатель'] == filters['consignee']]

    # Получаем нужные столбцы и преобразуем в желаемый формат
    result = filtered_data[['ID', 'leavingChance']].to_dict(orient='records')

    return result

 #Пример использования:
file_path = r'uploaded_files\test.xlsx'
query_params = {
    'isMSP': 'Да',
    'companySize': float('nan'),  # или np.nan, в зависимости от того, как задаете
    'cityActual': 'Муром',
    'shipper': 'Да',
    'consignee': 'Да'
}

output = filter_data(file_path, query_params)
print(output)
