import os
import pandas as pd
import dask.dataframe as dd
import glob
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle
import numpy as np

# 1. Поиск файла
def find_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

file_to_find = 'Объёмы перевозок.xls'
search_directory = 'uploaded_files'  # Changed to search in 'uploaded_files'
file_path = find_file(file_to_find, search_directory)

if file_path:
    print(f"Файл найден: {file_path}")
    data = pd.read_excel(file_path, header=2)  # Adjust header if necessary
else:
    print("Файл не найден.")

transportation_volumes = file_path

# 2. Фильтрация данных
input_file = transportation_volumes
output_file = r'uploaded_files\Объёмы_перевозок_filtered.xlsx'
data = pd.read_excel(input_file, header=1)
data.columns = data.columns.str.strip()
data.rename(columns={'Unnamed: 0': 'ID'}, inplace=True)
current_year = 2024
current_month = 10  
available_months = []

for year in range(current_year, 2019, -1):
    for month in range(12, 0, -1):
        month_str = f'{year}/{month:02d}'
        if month_str in data.columns and f'{month_str}.1' in data.columns:
            available_months.append(month_str)
            if len(available_months) == 12:
                break
    if len(available_months) == 12:
        break

if len(available_months) < 12:
    pass  # Handle insufficient months if needed
else:
    period_1 = available_months[:6]
    period_2 = available_months[6:12]

    провозная_плата_1 = data[period_1].sum(axis=1)
    объем_перевозок_1 = data[[f'{month}.1' for month in period_1]].sum(axis=1)
    провозная_плата_2 = data[period_2].sum(axis=1)
    объем_перевозок_2 = data[[f'{month}.1' for month in period_2]].sum(axis=1)

    results = {
        'ID': data['ID'],
        'Провозная плата (период 1)': провозная_плата_1.where(провозная_плата_1.notna(), None),
        'Объем перевозок(тн) (период 1)': объем_перевозок_1.where(провозная_плата_1.notna(), None),
        'Провозная плата (период 2)': провозная_плата_2.where(провозная_плата_2.notna(), None),
        'Объем перевозок(тн) (период 2)': объем_перевозок_2.where(провозная_плата_2.notna(), None),
    }

    result_df = pd.DataFrame(results)
    result_df.dropna(subset=['Провозная плата (период 1)', 'Объем перевозок(тн) (период 1)', 
                             'Провозная плата (период 2)', 'Объем перевозок(тн) (период 2)'], inplace=True)
    result_df.to_excel(output_file, index=False)

# 3. Убираем непотребства
file_path = r'uploaded_files\Объёмы_перевозок_filtered.xlsx'
df = pd.read_excel(file_path, header=1)  
df.columns = [
    'ID', 
    'Провозная плата (период 2)', 
    'Объем перевозок(тн) (период 2)', 
    'Провозная плата (период 1)', 
    'Объем перевозок(тн) (период 1)'
]

df_summary = df.groupby('ID').sum().reset_index()
output_path = r'uploaded_files\Объёмы_перевозок_filtered.xlsx'
df_summary.to_excel(output_path, index=False)

# 4. Подготовка данных + объединение
file_path = r'uploaded_files\Объёмы_перевозок_filtered.xlsx'
df_original = pd.read_excel(file_path)
df_original = dd.from_pandas(df_original, npartitions=1)
unique_ids = df_original['ID'].dropna().unique().compute()
dataframes = []

for file in glob.glob(r"uploaded_files\Выгрузка_маркетинговые списки\МС_*.xls"):
    df = pd.read_excel(file)
    df = dd.from_pandas(df, npartitions=1)
    filtered_df = df[df['ID'].isin(unique_ids)]
    dataframes.append(filtered_df)

if dataframes:  
    combined_df = dd.concat(dataframes, ignore_index=True)
else:
    combined_df = dd.from_pandas(pd.DataFrame(), npartitions=1)

final_df = df_original.merge(combined_df, on='ID', how='left')
final_df = final_df.compute()
output_path = r'uploaded_files\test.xlsx'
final_df.to_excel(output_path, index=False)

# 5. Фильтрация столбцов
file_path = r'uploaded_files\test.xlsx'
df = pd.read_excel(file_path)

selected_columns = [
    'ID',
    'Находится в реестре МСП',
    'Размер компании.Наименование',
    'Город фактический',
    'Грузоотправитель',
    'Грузополучатель',
    'Размер уставного капитала объявленный',
    'Численность персонала по данным ФНС.Количество',
    'Карточка клиента (внешний источник).Индекс платежной дисциплины Значение',
    'Карточка клиента (внешний источник).Индекс финансового риска Значение',
    'Провозная плата (период 1)',
    'Провозная плата (период 2)',
    'Объем перевозок(тн) (период 1)',
    'Объем перевозок(тн) (период 2)'
]

df_filtered = df[selected_columns]
df_filtered = df_filtered.drop_duplicates(subset='ID', keep='last')
output_path = r'uploaded_files\test.xlsx'
df_filtered.to_excel(output_path, index=False)

# 6. Удаление строк
file_path = r'uploaded_files\test.xlsx'
df = pd.read_excel(file_path)
df_cleaned = df[df['Находится в реестре МСП'].isin(['Да', 'Нет'])]
df_cleaned.to_excel(r'uploaded_files\test.xlsx', index=False)

# Подготовка данных
activity_file_path = r'uploaded_files\Выгрузки_интересы+обращения+объёмы перевозок\Обращения.xls'
activity_df = pd.read_excel(activity_file_path)
filtered_data_path = r'uploaded_files\test.xlsx'
filtered_df = pd.read_excel(filtered_data_path)

topics_of_interest = [
    "Цифровые сервисы",
    "Электронный обмен документами",
    "Перевозка грузов и порожних вагонов",
    "Оформление документов связанных с перевозкой грузов",
    "Заключение договоров",
    "Финансовые расчеты",
    "Перевозка грузов в контейнерах",
    "Благодарности",
    "Перевозка грузов в рефрижераторных секциях ИВ-термосах вагонах-термосах",
    "Перевозка сборной/мелкой партии грузов / разовая"
]

filtered_activity_df = activity_df[activity_df['Тема вопроса'].isin(topics_of_interest)]
positive_action_counts = filtered_activity_df['ID'].value_counts()
filtered_df['positive_action'] = filtered_df['ID'].map(positive_action_counts).fillna(0)

output_path = r'uploaded_files\test.xlsx'
filtered_df.to_excel(output_path, index=False)

# Предсказание для каждого ID
data_full = pd.read_excel(r'uploaded_files\test.xlsx')
df = pd.DataFrame(data_full)

with open(r'Models\random_forest_model.pkl', 'rb') as f:
    loaded_rf_model = pickle.load(f)

df[['Размер уставного капитала объявленный', 'Численность персонала по данным ФНС.Количество', 
    'Карточка клиента (внешний источник).Индекс платежной дисциплины Значение', 
    'Карточка клиента (внешний источник).Индекс финансового риска Значение',
    'Провозная плата (период 1)', 'Провозная плата (период 2)',
    'Объем перевозок(тн) (период 1)', 'Объем перевозок(тн) (период 2)',
    'positive_action']] = np.log1p(df[['Размер уставного капитала объявленный', 
    'Численность персонала по данным ФНС.Количество', 
    'Карточка клиента (внешний источник).Индекс платежной дисциплины Значение', 
    'Карточка клиента (внешний источник).Индекс финансового риска Значение',
    'Провозная плата (период 1)', 'Провозная плата (период 2)',
    'Объем перевозок(тн) (период 1)', 'Объем перевозок(тн) (период 2)',
    'positive_action']])

df = df[['ID', 'Размер уставного капитала объявленный', 'Численность персонала по данным ФНС.Количество', 
          'Карточка клиента (внешний источник).Индекс платежной дисциплины Значение', 
          'Карточка клиента (внешний источник).Индекс финансового риска Значение',
          'Провозная плата (период 1)', 'Провозная плата (период 2)',
          'Объем перевозок(тн) (период 1)', 'Объем перевозок(тн) (период 2)', 
          'positive_action']]

rf_predictions = loaded_rf_model.predict(df.drop(columns='ID'))
rf_predictions_normal = np.expm1(rf_predictions)

results = pd.DataFrame({
    'ID': df['ID'],
    'Predicted_Devotion_RF': rf_predictions_normal
})

results['leavingChance'] = 100 - results['Predicted_Devotion_RF']
test_data = pd.read_excel(r'uploaded_files\test.xlsx')
test_data = test_data.merge(results[['ID', 'leavingChance']], on='ID', how='left')
test_data.to_excel(r'uploaded_files\test.xlsx', index=False)
