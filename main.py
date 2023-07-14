# Приложение.exe на питоне для создания графика температур
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter
from tkinter.messagebox import showerror
import os
from matplotlib.backends.backend_pdf import PdfPages

# Создаем окно программы
root = tkinter.Tk()
root.title("App") 
root.geometry("680x500")
root.configure(bg="#FBFCFC")

def get_list_xticks(values: list, list_dates: list):
    """Формула расположения меток на графике"""
    value = int(len(values) / (len(list_dates)-1))
    count, list_xticks, result = 1, [], 0
    list_xticks.append(result)
    for _ in range(len(list_dates)-2):
        result = value * count
        list_xticks.append(result)
        count += 1
    list_xticks.append(len(values))
    return list_xticks[::-1]
            
def reader():
    """Подключение к csv файлу"""
    return pd.read_csv(
        'C:\Name\name_csv.csv', 
        delimiter=';',
        usecols=['VarValue', 'TimeString']
    )

def get_changes_value(value: str) -> int:
    """Получение измененого значения"""
    if value != '0':
        value = " ".join(value).split()[:-1]
        value = int("".join(value))
        return int(value)
    else:
        return int(value)

    
def find_var_value(date_time: datetime) -> float:
    """Поиск по дате"""
    file = reader() #Подключаемся к csv файлу
    row = file[file['TimeString'] == str(date_time)] # Проверка на дату
    return row['VarValue'].iloc[0] # Вывод значения

def show_error(): 
    """Вызов ошибки"""
    showerror(title="Ошибка", message="Ошибка в заполнении даты!")

def get_csv(datetime_1: datetime, datetime_2: datetime) -> list:
    """Поиск и вывод csv файла"""
    values = [] 
    for data in reader()['TimeString']:
        try:
            date_time = datetime.strptime(data, "%d.%m.%Y %H:%M:%S") # Превраещаем в дату
        except:
            pass
        else:
            if datetime_1 <= date_time <= datetime_2: # Сравниваем даты
                var_value = find_var_value(data) # Вытаскиваем value 
                value = get_changes_value(str(var_value))
                values.append(value)
    return values[::-1]

def change_datetime(datetime: str) -> str:
    """Изменеям дату"""
    month_day = datetime.split()[0].split('.')
    hour = datetime.split()[1].split(':')[0]
    date = f'{month_day[1]}{month_day[0]}{hour}'
    return date

def get_list_datatime(datetime_1: datetime, datetime_2: datetime) -> list:
    """Создание списка дат и времени"""
    hours = int((datetime_2 - datetime_1).seconds / 3600) # Узнаем сколько часов
    if hours >= 24:
        list_datetime = pd.date_range(start=datetime_1, end=datetime_2, freq='D').tolist()
    if hours >= 12:
        list_datetime = pd.date_range(start=datetime_1, end=datetime_2, freq='3H').tolist()
    else:
        list_datetime = pd.date_range(start=datetime_1, end=datetime_2, freq='H').tolist()
    if hours >= 24:
        list_dates = [str(_).split()[0] for _ in list_datetime]
    else:
        list_dates = [str(_).split()[1] for _ in list_datetime]
    return list_dates

def graph(values: list, list_datatime: list,
    datetime_1: datetime, datetime_2: datetime) -> None:
    """Создание графика"""
    fig, ax = plt.subplots()
    sns.lineplot(data=values, ax=ax)
    ax.set_xticks(get_list_xticks(values, list_datatime))
    ax.set_xticklabels(list_datatime, rotation=45) # Ставим на x значения
    ax.set_yticks([0, 20, 50, 80, 100]) # Ставим на y значения
    ax.set_yticklabels([0.0, 20.0, 50.0, 80.0, 100.0])
    plt.xlabel(f"От {datetime_1} До {datetime_2}")
    plt.tight_layout()

def get_datatime():
    """Получение данных из текстовых полей"""
    data_1 = year_1.get()
    data_2 = year_2.get()
    months_1 = month_1.get()
    months_2 = month_2.get()
    days_1 = day_1.get()
    days_2 = day_2.get()
    times_1 = time_1.get() 
    times_2 = time_2.get()

    # Соединяем данные
    data_time_1 = f"{days_1}.{months_1}.{data_1} {times_1}:00:00"
    data_time_2 = f"{days_2}.{months_2}.{data_2} {times_2}:00:00"
    return data_time_1, data_time_2

def create_graph():
    """Получение времени и вывод графика"""
    data_time_1, data_time_2 = get_datatime() # Получение данных из текстовых полей
    try:
        datetime_1 = datetime.strptime(data_time_1, "%d.%m.%Y %H:%M:%S")
        datetime_2 = datetime.strptime(data_time_2, "%d.%m.%Y %H:%M:%S") 
    except ValueError:
        show_error() # Вызываем оповещение о ошибке
    else:
        values = get_csv(datetime_1, datetime_2) # Получаем данные из csv файла по дате и времени
        list_datatime = get_list_datatime(datetime_1, datetime_2) # Получаем даты и время в виде списка
        graph(values, list_datatime, datetime_1, datetime_2) # Создание графика 
        return str(data_time_1), str(data_time_2)
        
def button_get():
    """Кнопка Вывода"""
    create_graph()
    plt.show()

def button_save():
    """Кнопка сохранения"""
    data_time_1, data_time_2 = create_graph()
    data_time_1 = change_datetime(data_time_1)
    data_time_2 = change_datetime(data_time_2)
    plt.savefig(f'C:\Name\{data_time_1}_{data_time_2}.pdf') # Указываем куда сохранять pdf файл


# Создание загаловков
label_1 = tkinter.Label(
    root,
    text="Начало Даты",
    bg="#FBFCFC",
    fg='#1F1F21',
    font=('Shentox ', 15)
)
label_2 = tkinter.Label(
    root,
    bg="#FBFCFC",
    text="Конец Даты",
    fg='#1F1F21',
    font=('Shentox ', 15)
)

# Создание текстовых полей
default = tkinter.StringVar(root, value='2023')
year_1 = tkinter.Entry(justify="center", relief="sunken", textvariable=default)
year_2 = tkinter.Entry(justify="center", relief="sunken", textvariable=default)
month_1 = tkinter.Entry(justify="center", relief="sunken")
month_2 = tkinter.Entry(justify="center", relief="sunken")
day_1 = tkinter.Entry(justify="center", relief="sunken")
day_2 = tkinter.Entry(justify="center", relief="sunken")
time_1 = tkinter.Entry(justify="center", relief="sunken")
time_2 = tkinter.Entry(justify="center", relief="sunken")

# Создание Меток
lbl_data_1 = tkinter.Label(text="Дата")
lbl_data_2 = tkinter.Label(text="Дата")
lbl_month_1 = tkinter.Label(text="Месяц")
lbl_month_2 = tkinter.Label(text="Месяц")
lbl_day_1 = tkinter.Label(text="День")
lbl_day_2 = tkinter.Label(text="День")
lbl_time_1 = tkinter.Label(text="Час")
lbl_time_2 = tkinter.Label(text="Час")

# Создание кнопок
btn = tkinter.Button(
    text="Вывод",
    bg="#000000",
    fg="#FFFFFF",
    font=('Shentox ', 13),
    command=button_get
)

btn_2 = tkinter.Button(
    text="Печать",
    bg="#000000",
    fg="#FFFFFF",
    font=('Shentox ', 13),
    command=button_save
)

# Загаловки
label_1.place(x=150, y=60)
label_2.place(x=400, y=60)

# Текстовые поля
year_1.place(x=200, y=150, width=50, height=20)
year_2.place(x=450, y=150, width=50, height=20)
month_1.place(x=200, y=200, width=50, height=20)
month_2.place(x=450, y=200, width=50, height=20)
day_1.place(x=200, y=250, width=50, height=20)
day_2.place(x=450, y=250, width=50, height=20)
time_1.place(x=200, y=300, width=50, height=20)
time_2.place(x=450, y=300, width=50, height=20)

# Метки
lbl_data_1.place(x=150, y=150, width=50, height=20)
lbl_data_2.place(x=400, y=150, width=50, height=20)
lbl_month_1.place(x=150, y=200, width=50, height=20)
lbl_month_2.place(x=400, y=200, width=50, height=20)
lbl_day_1.place(x=150, y=250, width=50, height=20)
lbl_day_2.place(x=400, y=250, width=50, height=20)
lbl_time_1.place(x=150, y=300, width=50, height=20)
lbl_time_2.place(x=400, y=300, width=50, height=20)

# Кнопка 
btn.place(x=400, y=400)
btn_2.place(x=150, y=400)

# Запуск приложения
root.mainloop()

