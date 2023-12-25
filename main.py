import PySimpleGUI as sg
import pickle

# Определение имени файла для сохранения данных
data_file = 'my_list_data.pkl'

# Загрузка сохраненных данных, если они есть
try:
    with open(data_file, 'rb') as file:
        my_list = pickle.load(file)
except FileNotFoundError:
    my_list = []

# Определение графического интерфейса
layout = [
    [sg.InputText(key='-INPUT-'), sg.Button('Добавить')],
    [sg.Listbox(values=my_list, size=(30, 5), key='-LIST-', enable_events=True),
     sg.Column([
         [sg.Button('Просмотр', key='-VIEW-', disabled=True)],
         [sg.Button('Редактировать', key='-EDIT-', disabled=True)],
         [sg.Button('Удалить', key='-DELETE-', disabled=True)]
     ])],
]

# Создание окна
window = sg.Window('Пример списка', layout)

# Обработка событий
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        # Сохранение данных перед выходом
        with open(data_file, 'wb') as file:
            pickle.dump(my_list, file)
        break
    elif event == 'Добавить':
        item = values['-INPUT-']
        if item:
            my_list.append(item)
            window['-LIST-'].update(values=my_list)
    elif event == '-LIST-':
        if values['-LIST-']:
            selected_item = values['-LIST-'][0]
            try:
                selected_index = my_list.index(selected_item)
                window['-VIEW-'].update(disabled=False)
                window['-EDIT-'].update(disabled=False)
                window['-DELETE-'].update(disabled=False)
            except ValueError:
                # Если выбранный элемент не найден в списке, игнорируем его
                pass
    elif event == '-VIEW-':
        if values['-LIST-']:
            sg.popup(f'Выбранный элемент: {values["-LIST-"][0]}')
    elif event == '-EDIT-':
        if values['-LIST-']:
            new_item = sg.popup_get_text('Введите новое значение', default_text=values['-LIST-'][0])
            if new_item is not None:
                my_list[selected_index] = new_item
                window['-LIST-'].update(values=my_list)
    elif event == '-DELETE-':
        if values['-LIST-']:
            my_list.remove(values['-LIST-'][0])
            window['-LIST-'].update(values=my_list)
            window['-VIEW-'].update(disabled=True)
            window['-EDIT-'].update(disabled=True)
            window['-DELETE-'].update(disabled=True)

# Закрытие окна
window.close()
