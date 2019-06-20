import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
    # import PySimpleGUIWeb as sg       # take your pick of ports. Runs on both
else:
    import PySimpleGUI27 as sg
import random
import string

tam = 25
layout = [
            [sg.Text('SOPA DE LETRAS'), sg.Text('', key='_OUTPUT_')],
            [sg.Graph((500,500), (0,300), (300,0), key='_GRAPH_', change_submits=True)],
            [sg.Button('Exit')]
         ]

window = sg.Window('Window Title', ).Layout(layout).Finalize()

g = window.FindElement ('_GRAPH_')
for fila in range(10):
    for columna in range (10):
        g.DrawRectangle ((columna * tam + 5, fila * tam + 3 ), (columna * tam + tam + 5 , fila * tam + tam + 3), line_color = 'black')
        g.DrawText ('A',(columna * tam + 20, fila * tam + 20), font = ("Helvetica", 16))                  
while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    mouse = values['_GRAPH_']
    if event == '_GRAPH_':
        box_x = mouse[0]//tam
        box_y = mouse[1]//tam
        locacion = (box_x + tam +18, box_y * tam + 17)
        g.DrawOval(top_left, bottom_rigth, fill_color = 'green')
window.Close()    
