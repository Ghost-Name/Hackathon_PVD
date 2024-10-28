# Описание файлов
## filter_bd.py - должен находится в той же директории, что и папка uploaded_files
1) фильтрует маркетинговые списки по клиентам имеющие ЕЛС, выбирает параметры для предсказания
2) использует Обращения.xls и Объёмы перевозок.xls для сбора оставшихся параметров и создания доп. параметров
3) использует random_forest_model.pkl из папки Models в директории вместе с исполняемым файлом
4) создаёт test.xlsx с предсказанной вероятностью ухода клиента

## после окончания выполнения файла filter_bd.py в консоли будет высвечено сообщение: Файл test.xlsx создан в uploaded_files
![Table](https://github.com/Ghost-Name/Hackathon_PVD/blob/PNG/PNG/table.png)

## start_ml.py - самостоятельно находит файл test.xlsx.
1) пример ввода параметров фильтра приложен в самом фале
2) вывод: ID клиента и его вероятность ухода в процентах

![Console](https://github.com/Ghost-Name/Hackathon_PVD/blob/PNG/PNG/start_ml.png)

