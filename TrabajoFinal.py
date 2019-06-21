import PySimpleGUI as sg
from pattern.es import parse, split
from pattern.web import Wiktionary
import json
import random
import string

engine = Wiktionary(license=None, language='es')
dic = {'lista': [], 'sustantivo': [], 'adjetivo':[], 'verbo': [], 'reporte': [], 'def':{}}
sustantivos = []
adjetivos = []
verbos = []
defi = []

def verificar_palabra(palabra, dic):
    claves = {'NN': 'sustantivo' , 'JJ' : 'adjetivo' , 'VB': 'verbo'}
    try:
        article = engine.search(palabra)
        eti = article.sections[3].title.lower().split(' ')[0]
        print(eti)
        dic[eti].append(palabra)
        dic['lista'].append(palabra)
        dic['def'].update({palabra:article.sections[3].content})
        if ((claves[parse(palabra).split()[0][0][1]] != eti)):
            dic['reporte'].append('La palabra {} no coincide con pattern.es'. format(palabra))
    except AttributeError:
        if (parse(palabra).split()[0][0][1] in dic):
            text = sg.PopupGetText('Definición local', '')
            dic['def'].update({palabra:text})
            dic['reporte'].append('La palabra {} no coincide con Wiktionary\n Se utilizará una definición guardada en un archivo local'.format(palabra))
            sg.Popup('ADVERTENCIA!', 'Se utilizará una definición guardada en un archivo local')
        else:
            dic['reporte'].append('No se encuentra la palabra {} en ningun recurso'.format(palabra))
    except KeyError:
        sg.Popup('ADVERTENCIA!', 'No esta ingresando ningun sustantivo, adjetivo o verbo')
        dic['reporte'].append('La palabra {} no es ningun sustantivo, adjetivo o verbo'.format(palabra))
    return dic

def eliminarDelDic(palabra, dic):
    dic['lista'].remove(palabra)
    article = engine.search(palabra)
    eti = article.sections[3].title.lower().split(' ')[0]
    dic[eti].remove(palabra)
    dic['def'].pop(palabra)
    return dic

def redactar_reporte(lista):
    if (len(lista) == 0):
        texto = 'No hay reportes'
    else:
        for reporte in lista:
            texto = reporte + '\n'
    return texto

def abrir_archivo():
    lista = []
    while True:
        try:
            filename = sg.PopupGetFile('Abrir', no_window = True, file_types = (("JSON Files", "*.json"), ))
            if (filename != ''):
                lista.append(filename)
                with open(filename, "r") as infile:
                        aux = json.load(infile)[0]
                lista.append(aux)
            break
        except PermissionError:
            sg.PopupOK('No tiene permisos para abrir este archivo')
    return lista

def juego (sus, adj, verb, defi, mayus, H, ayDef, ayListPal, lyf):
    tam_pal = 0
    BOX_SIZE = 25
    lista = sus[:]
    lista.extend(adj)
    lista.extend(verb)
    for i in lista:
        if tam_pal < len(i):
            tam_pal = len(i)
    
    layout = [
            [sg.Text('SOPA DE LETRAS'), sg.Text('Sustantivos: {}'.format(len(sus))), sg.Text('Adjetivos: {}'.format(len(adj))), sg.Text('Verbos: {}'.format(len(verb))),],
            [sg.Graph((500,500), (0,300), (300,0), key='_GRAPH_', change_submits=True)],
            [sg.Listbox(lista, size=(30,6), visible= ayListPal), sg.Multiline("", key='def', visible= ayDef), sg.Button('Sig.\n definición', visible= ayDef)],
            [sg.Button('Salir')]
         ]

    window = sg.Window('Window Title', ).Layout(layout).Finalize()

    g = window.FindElement ('_GRAPH_')
    
    if H == True:
        for row in range(len(lista)*2):
            for col in range(tam_pal+3):
                    g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black')
        k = 0
        for row in range(len(lista)*2):
            if k < (len(lista)//2):
                fila = random.choice([True, False])
            else:
                fila = True
            i = 0
            j = 0
            palabra = ''
            for col in range(tam_pal+3):
                columna = False
                if fila == True:
                    columna = random.choice([True, False])
                else:
                    k+=1
                if (columna == True) or (fila == True and j == 3):
                    if len(lista) != 0:
                        palabra = random.choice(lista)
                        lista.remove(palabra)
                    columna = False
                if (i < len(palabra)) and (len(palabra) != 0):
                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                    g.DrawText('{}'.format(palabra[i]), letter_location, font='Courier 25')
                    i+=1 
                    fila = False
                else:
                    if mayus == True:
                        letra = random.choice(string.ascii_uppercase)
                    else:
                        letra = random.choice(string.ascii_lowercase)
                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                    g.DrawText('{}'.format(letra), letter_location, font='Courier 25')
                    j+=1
    else:
        for col in range(len(lista)*2):
            for row in range(tam_pal+3):
                    g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black')
        k = 0
        for col in range(len(lista)*2):
            if k < (len(lista)//2):
                fila = random.choice([True, False])
            else:
                fila = True
            i = 0
            j = 0
            palabra = ''
            for row in range(tam_pal+3):
                columna = False
                if fila == True:
                    columna = random.choice([True, False])
                else:
                    k+=1
                if (columna == True) or (fila == True and j == 3):
                    if len(lista) != 0:
                        palabra = random.choice(lista)
                        lista.remove(palabra)
                    columna = False
                if (i < len(palabra)) and (len(palabra) != 0):
                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                    g.DrawText('{}'.format(palabra[i]), letter_location, font='Courier 25')
                    i+=1 
                    fila = False
                else:
                    if mayus == True:
                        letra = random.choice(string.ascii_uppercase)
                    else:
                        letra = random.choice(string.ascii_lowercase)
                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                    g.DrawText('{}'.format(letra), letter_location, font='Courier 25')
                    j+=1

    h = 0
    while True:
        event, values = window.Read()
        print(event, values)
        mouse = values['_GRAPH_']
        if event == None or event == 'Salir':
            window.Close()
            break
        if event == 'Sig.\n definición':
            window.FindElement ('def').Update(value= defi[h])
            h+=1
            if h == len(defi):
                h = 0
        
        
                
            





tipografias = ('Arial', 'Courier', 'Comic', 'Fixedsys', 'Times', 'Verdana', 'Helvetica')
oficinas = ('Oficina 1', 'Oficina 2')
lista = []
lista2 = []

layout1 = [
    [sg.InputText(default_text="", key = 'ingreso')],
    [sg.Listbox(lista,size=(30, 6), key='lista' ),sg.Column([[sg.Button('Agregar')],[sg.Button('Eliminar')]])],
    [sg.Frame('Sustantivos', [[sg.Column([[sg.Spin([i for i in range(len(dic['sustantivo']))], initial_value=0, size= (15,1), key='cantSus')],[sg.ColorChooserButton('Color Sustantivos')]])]]), sg.Frame('Adjetivos', [[sg.Column([[sg.Spin([i for i in range(len(dic['adjetivo']))], initial_value=0, size= (15,1), key='cantAdj')],[sg.ColorChooserButton('Color Adjetivos')]])]]), sg.Frame('Verbos', [[sg.Column([[sg.Spin([i for i in range(len(dic['verbo']))], initial_value=0, size= (15,1), key = 'cantVerb')],[sg.ColorChooserButton('Color Verbos')]])]])],
    [sg.Frame('Orientiacion',[[sg.Column([[sg.Radio('Horizontal', "ORIENTACION", default=True, key='H')],[sg.Radio('Vertical', "ORIENTACION", key='V')]])]]), sg.Frame('Vista',[[sg.Column([[sg.Radio('Mayúsculas', "MAYUSMINUS", default=True, key='mayus')],[sg.Radio('Minúsculas', "MAYUSMINUS", key='minus')]])]]), sg.Frame('Ayuda', [[sg.Column([[sg.Checkbox('Definiciones', key='ayDef')],[sg.Checkbox('Lista de Palabras', key='ayListPal')]])]])],
    [sg.Frame('Reporte', [[sg.Frame('Titulo', [[sg.InputCombo(tipografias, size=(20, 1), key='tipoTit')]]), sg.Frame('Texto', [[sg.InputCombo(tipografias, size=(20, 1), key='tipoTex')]]), sg.Button('Generar reporte')]])],
    [sg.Checkbox('Look & feel', key='l&f'), sg.InputCombo(oficinas, size=(20, 1), key='ofi'), sg.Button('Abrir'), sg.Text('', key='dir')],
    [sg.Button('Jugar'), sg.Button('Salir')]
    ]

window = sg.Window('Trabajo Final').Layout(layout1)

while True:
    event, values = window.Read()
    print(values)
    if event == None or event == 'Salir':
        window.Close()
        break
    if event == 'Agregar':
        if values['ingreso'] != '':
            dic = verificar_palabra(values['ingreso'], dic)
            window.FindElement('lista').Update(dic['lista'])
            window.FindElement('ingreso').Update('')
            window.FindElement('cantSus').Update(values=[i for i in range(len(dic['sustantivo'])+1)])
            window.FindElement('cantAdj').Update(values=[i for i in range(len(dic['adjetivo'])+1)])
            window.FindElement('cantVerb').Update(values=[i for i in range(len(dic['verbo'])+1)])
    if event == 'Eliminar':
        if values['lista'] != []:
            dic = eliminarDelDic(values['lista'][0], dic)
            window.FindElement('lista').Update(dic['lista'])
    if event == 'Generar reporte':
        texto = redactar_reporte(dic['reporte'])
        layout2 = [
            [sg.Text('Reporte', font= values['tipoTit'])],
            [sg.Text(texto, font= values['tipoTex'])]
            ]
        window2 = sg.Window('Reporte').Layout(layout2)
        button, valor = window2.Read()
        window2.Close()
    if event == 'Abrir':
        arch = abrir_archivo()
        window.FindElement('ofi').Update(values=list(arch[1].keys()))
        window.FindElement('dir').Update(arch[0])
    if event == 'Jugar':
        if values['cantSus'] != '0':
            for i in (range(int(values['cantSus']))):
                palabra = dic['sustantivo'].pop(random.randrange(len(dic['sustantivo'])))
                if values['mayus'] == True:
                    sustantivos.append(palabra.upper())
                else:
                    sustantivos.append(palabra.lower())
                defi.append(dic['def'][palabra])
        if values['cantAdj'] != '0':
            for j in (range(int(values['cantAdj']))):
                palabra = dic['adjetivo'].pop(random.randrange(len(dic['adjetivo'])))
                if values['mayus'] == True:
                    adjetivos.append(palabra.upper())
                else:
                    adjetivos.append(palabra.lower())
                defi.append(dic['def'][palabra])
        if values['cantVerb'] != '0':
            for k in (range(int(values['cantVerb']))):
                palabra = dic['verbo'].pop(random.randrange(len(dic['verbo'])))
                if values['mayus'] == True:
                    adjetivos.append(palabra.upper())
                else:
                    adjetivos.append(palabra.lower())
                defi.append(dic['def'][palabra])
        window.Close()
        juego(sustantivos, adjetivos, verbos, defi, values['mayus'], values['H'], values['ayDef'], values['ayListPal'], values['l&f'])
        break

        
        

