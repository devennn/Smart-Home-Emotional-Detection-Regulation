import PySimpleGUI as sg

def setup_window(graph):

    # Layout
    image_layout = [sg.Image(filename='', key='image', size=(320, 240),
                    background_color='#000000')]

    logs = [sg.Output(size=(43,15), key='-OUTPUT-',background_color='#000000', text_color='white')]

    side_layout = [[graph],[sg.Button('Real-Time', size=(10, 1), font='Helvetica 10'),
                    sg.Button('Summary', size=(10, 1), font='Helvetica 10'),
                    sg.Button('10 Minutes', size=(10, 1), font='Helvetica 10')]]

    app_layout = [[sg.Checkbox('Table Lamp', size=(9,1), key='table_lamp', font='Helvetica 9'),
                    sg.Checkbox('Light 1', size=(9,1), key='bed_light', font='Helvetica 9'),
                    sg.Checkbox('TV', size=(9,1), key='tv', font='Helvetica 9')],
                  [sg.Checkbox('Front Door', size=(9,1), key='front_door', font='Helvetica 9'),
                    sg.Checkbox('Garage', size=(9,1), key='garage', font='Helvetica 9'),
                    sg.Checkbox('Fridge', size=(9,1), key='fridge', font='Helvetica 9')]]

    time_list = ['10 sec', '30 sec', '1 min', '5 min', '10 min'] #in seconds
    choose_time_layout = [[sg.Text('Period'+':', justification='l', size=(10,1)),
                            sg.Combo(time_list, size=(10, 10), default_value=time_list[2],
                            key='time', background_color='#000000', text_color='white')],
                            [sg.Text("Telegram"+':', justification='l', size=(10,1)),
                            sg.Input(key='chat_id', justification='l', size=(10,1),
                            background_color='#000000', text_color='white'),
                            sg.Button('Connect')]]

    main_button_layout = [sg.Button('Start', size=(7, 1), font='Helvetica 14'),
                            sg.Button('Stop', size=(7, 1), font='Helvetica 14'),
                            sg.Button('Exit', size=(7, 1), font='Helvetica 14')]

    # Column 1
    column1 = [[sg.Frame('Data', side_layout)],[sg.Frame('Application', app_layout)],
                [sg.Frame('Send Data', choose_time_layout)]]

    tab1 = sg.Tab('Stream', [image_layout])
    tab2 = sg.Tab('Backlogs', [logs])
    tabgroup = [sg.TabGroup([[tab1, tab2]])]

    # define the window layout
    layout = [[sg.Frame('Output', [tabgroup, main_button_layout]), sg.Column(column1)]]

    return sg.Window('Smart Home', layout, location=(800, 400))
