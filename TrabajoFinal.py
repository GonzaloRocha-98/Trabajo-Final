import PySimpleGUI as sg
from pattern.es import parse, split
from pattern.web import Wiktionary
import json
import random
import string

engine = Wiktionary(license=None, language='es')
<<<<<<< HEAD
=======
dic = {'lista': [], 'sustantivo': [], 'adjetivo':[], 'verbo': [], 'reporte': [], 'def':{}}
sustantivos = []
adjetivos = []
verbos = []
defi = []
>>>>>>> 029884f036ce91b6f844bb743d5e6d6addd30d52

class Palabras():

    def __init__(self, pal, clase, defi):
        self.__pal = pal
        self.__clase = clase
        self.__defi = defi
        self.__cord = {}

    def getPal(self):
        return self.__pal

    def getClase(self):
        return self.__clase

    def getDefi(self):
        return self.__defi

    def getCord(self):
        return self.__cord

    def aMayus(self):
        self.__pal = self.__pal.upper()

    def aMinus(self):
        self.__pal = self.__pal.lower()

    def setCord(self, cord, letra):
        self.__cord.update({cord:letra})




    

def verificar_palabra(palabra, dic, reporte):
    claves = {'NN': 'sustantivo' , 'JJ' : 'adjetivo' , 'VB': 'verbo'}
    try:
        article = engine.search(palabra)
        eti = article.sections[3].title.lower().split(' ')[0]
        print(eti)
        obj = Palabras(palabra, eti, article.sections[3].content)
        dic.append(obj)
        if ((claves[parse(palabra).split()[0][0][1]] != eti)):
            reporte.append('La palabra {} no coincide con pattern.es'. format(palabra))
    except AttributeError:
        if (parse(palabra).split()[0][0][1] in claves):
            text = sg.PopupGetText('Definición local', '')
            obj = Palabras(palabra, parse(palabra).split()[0][0][1], text)
            dic.append(obj)
            reporte.append('La palabra {} no coincide con Wiktionary\n Se utilizará una definición guardada en un archivo local'.format(palabra))
            sg.Popup('ADVERTENCIA!', 'Se utilizará una definición guardada en un archivo local')
        else:
            reporte.append('No se encuentra la palabra {} en ningun recurso'.format(palabra))
    except KeyError:
        sg.Popup('ADVERTENCIA!', 'No esta ingresando ningun sustantivo, adjetivo o verbo')
        reporte.append('La palabra {} no es ningun sustantivo, adjetivo o verbo'.format(palabra))
    return dic, reporte

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

<<<<<<< HEAD
def juego (lis, sus, adj, verb, colorSus, colorAdj, colorVerb, mayus, H, ayDef, ayListPal, lyf):
    tam_pal = 0
    lista = []
    total = len(lis)
    c = 0
    cont = 0
    pos = {}
    color= '#ffffff'
    BOX_SIZE = 25
    for i in lis:
        if tam_pal < len(i.getPal()):
            tam_pal = len(i.getPal())
    total_letras = (total*2)*(tam_pal+3)
    print(tam_pal)
    print(len(lis))
    layout = [
            [sg.Text('SOPA DE LETRAS'), sg.Text('Sustantivos: {}'.format(sus)), sg.Text('Adjetivos: {}'.format(adj)), sg.Text('Verbos: {}'.format(verb)),],
            [sg.Graph((500,500), (0,300), (300,0), key='_GRAPH_', change_submits=True), sg.Column([[sg.Button('Sustantivos')], [sg.Button('Adjetivos')], [sg.Button('Verbos')]])],
            [sg.Listbox([i.getPal() for i in lis], size=(30,6), visible= ayListPal), sg.Multiline("", key='def', visible= ayDef), sg.Button('Sig.\n definición', visible= ayDef)],
            [sg.Button('Salir'), sg.Button('Verificar')]
         ]

    window = sg.Window('Window Title', ).Layout(layout).Finalize()

    g = window.FindElement ('_GRAPH_')
    
    if H == True:
        for row in range(total*2):
            for col in range(tam_pal+3):
                    g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color= '#ffffff')
                    pos.update({(col,row):['#ffffff']})
        k = 0
        for row in range(total*2):
            if k < (total//2):
                fila = random.choice([True, False])
                if fila == False:
                    k+=1
>>>>>>> 029884f036ce91b6f844bb743d5e6d6addd30d52
            else:
                fila = True
            i = 0
            j = 0
            palabra = ''
            for col in range(tam_pal+3):
                columna = False
                if fila == True:
<<<<<<< HEAD
                    columna = random.choice([True, False])                    
                if (columna == True) or (fila == True and j == 3):
                    if c < total:
                        ren = random.randrange(len(lis))
                        lista.append(lis.pop(ren))
                        palabra = lista[-1].getPal()
                        c+=1
                    columna = False
                if (i < len(palabra)) and (len(palabra) != 0):
                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                    lista[-1].setCord((col, row), palabra[i])
                    g.DrawText('{}'.format(palabra[i]), letter_location, font='Courier 25')
                    pos[(col,row)].append(palabra[i])
>>>>>>> 029884f036ce91b6f844bb743d5e6d6addd30d52
                    i+=1 
                    fila = False
                else:
                    if mayus == True:
                        letra = random.choice(string.ascii_uppercase)
                    else:
                        letra = random.choice(string.ascii_lowercase)
                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                    g.DrawText('{}'.format(letra), letter_location, font='Courier 25')
<<<<<<< HEAD
                    pos[(col,row)].append(letra)
                    cont+=1
                    j+=1
    else:
        for col in range(total*2):
            for row in range(tam_pal+3):
                    g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color= '#ffffff')
                    pos.update({(col,row):['#ffffff']})
                    print(pos)
        k = 0
        for col in range(total*2):
            if k != (total//2):
                columna = random.choice([True, False])
                if columna == False:
                    k+=1
>>>>>>> 029884f036ce91b6f844bb743d5e6d6addd30d52
            else:
                fila = True
            i = 0
            j = 0
            palabra = ''
            for row in range(tam_pal+3):
<<<<<<< HEAD
                fila = False
                if columna == True:
                    fila = random.choice([True, False])
                if (fila == True) or (columna == True and j == 3):
                    if c < total:
                        ren = random.randrange(len(lis))
                        lista.append(lis.pop(ren))
                        palabra = lista[-1].getPal()
                        c+=1
                    fila = False
                if (i < len(palabra)) and (len(palabra) != 0):
                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                    lista[-1].setCord((col, row), palabra[i])
                    g.DrawText('{}'.format(palabra[i]), letter_location, font='Courier 25')
                    pos[(col,row)].append(palabra[i])
                    i+=1 
                    columna = False
>>>>>>> 029884f036ce91b6f844bb743d5e6d6addd30d52
                else:
                    if mayus == True:
                        letra = random.choice(string.ascii_uppercase)
                    else:
                        letra = random.choice(string.ascii_lowercase)
                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                    g.DrawText('{}'.format(letra), letter_location, font='Courier 25')
<<<<<<< HEAD
                    pos[(col,row)].append(letra)
                    cont+=1
                    j+=1
    next_color = '#ffffff'
    h = 0
    while True:
        event, values = window.Read()
        print(pos)
>>>>>>> 029884f036ce91b6f844bb743d5e6d6addd30d52
        print(event, values)
        mouse = values['_GRAPH_']
        if event == None or event == 'Salir':
            window.Close()
            break
        if event == 'Sig.\n definición':
<<<<<<< HEAD
            window.FindElement ('def').Update(value= lista[h].getDefi())
            h+=1
            if h == len(lista):
                h = 0
        if event == '_GRAPH_':
            if mouse == (None, None):
                continue
            box_x = mouse[0]//BOX_SIZE
            box_y = mouse[1]//BOX_SIZE
            if pos[(box_x,box_y)][0] == color:
                next_color = '#ffffff'
            else:
                next_color = color
            g.DrawRectangle((box_x * BOX_SIZE + 5, box_y * BOX_SIZE + 3), (box_x * BOX_SIZE + BOX_SIZE + 5, box_y * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color= next_color)
            pos[(box_x,box_y)][0] = next_color
            letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
            g.DrawText('{}'.format(pos[(box_x,box_y)][1]), letter_location, font='Courier 25')
        if event == 'Sustantivos':
            color = colorSus
        if event == 'Adjetivos':
            color = colorAdj
        if event == 'Verbos':
            color = colorVerb
        if event == 'Verificar':
            if H == True:
                i = 0
                ganar = True
                for row in range(total*2):
                    sig = False
                    for col in range(tam_pal+3):
                        if (col,row) in lista[i].getCord():
                            sig = True
                            if lista[i].getClase() == 'sustantivo':
                                if (pos[(col,row)][0] != colorSus) and (pos[(col,row)][0] != '#ffffff'):
                                    pos[(col,row)][0] = '#ffffff'
                                    g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color= pos[(col,row)][0])
                                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                                    g.DrawText('{}'.format(pos[(col,row)][1]), letter_location, font='Courier 25')
                                elif (pos[(col,row)][0] == colorSus) and (total_letras != cont):
                                    total_letras-=1
                            if lista[i].getClase() == 'adjetivo':
                                if (pos[(col,row)][0] != colorAdj) and (pos[(col,row)][0] != '#ffffff'):
                                    pos[(col,row)][0] = '#ffffff'
                                    g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color= pos[(col,row)][0])
                                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                                    g.DrawText('{}'.format(pos[(col,row)][1]), letter_location, font='Courier 25')
                                elif (pos[(col,row)][0] == colorAdj) and (total_letras != cont):
                                    total_letras-=1
                            if lista[i].getClase() == 'verbo':
                                if (pos[(col,row)][0] != colorVerb) and (pos[(col,row)][0] != '#ffffff'):
                                    pos[(col,row)][0] = '#ffffff'
                                    g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color= pos[(col,row)][0])
                                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                                    g.DrawText('{}'.format(pos[(col,row)][1]), letter_location, font='Courier 25')
                                elif (pos[(col,row)][0] == colorVerb) and (total_letras != cont):
                                    total_letras-=1
                        elif (pos[(col,row)][0] != '#ffffff'):
                            pos[(col,row)][0] = '#ffffff'
                            g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color= pos[(col,row)][0])
                            letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                            g.DrawText('{}'.format(pos[(col,row)][1]), letter_location, font='Courier 25')
                            ganar = False
                    if (sig == True) and (i < (len(lista)-1)):
                        i+=1
                if (total_letras == cont) and (ganar == True):
                    sg.Popup('FELICITACIONES!!! GANASTE!')
            else:
                i = 0
                ganar = True
                for col in range(total*2):
                    sig = False
                    for row in range(tam_pal+3):
                        if (col,row) in lista[i].getCord():
                            sig = True
                            if lista[i].getClase() == 'sustantivo':
                                if (pos[(col,row)][0] != colorSus) and (pos[(col,row)][0] != '#ffffff'):
                                    pos[(col,row)][0] = '#ffffff'
                                    g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color= pos[(col,row)][1])
                                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                                    g.DrawText('{}'.format(pos[(col,row)][1]), letter_location, font='Courier 25')
                                elif (pos[(col,row)][0] == colorSus) and (total_letras != cont):
                                    total_letras-=1
                            if lista[i].getClase() == 'adjetivo':
                                if (pos[(col,row)][0] != colorAdj) and (pos[(col,row)][0] != '#ffffff'):
                                    pos[(col,row)][0] = '#ffffff'
                                    g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color= pos[(col,row)][1])
                                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                                    g.DrawText('{}'.format(pos[(col,row)][1]), letter_location, font='Courier 25')
                                elif (pos[(col,row)][0] == colorAdj) and (total_letras != cont):
                                    total_letras-=1
                            if lista[i].getClase() == 'verbo':
                                if (pos[(col,row)][0] != colorVerb) and (pos[(col,row)][0] != '#ffffff'):
                                    pos[(col,row)][0] = '#ffffff'
                                    g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color= pos[(col,row)][1])
                                    letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                                    g.DrawText('{}'.format(pos[(col,row)][1]), letter_location, font='Courier 25')
                                elif (pos[(col,row)][0] == colorVerb) and (total_letras != cont):
                                    total_letras-=1
                        elif (pos[(col,row)][0] != '#ffffff'):
                            pos[(col,row)][0] = '#ffffff'
                            g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color= pos[(col,row)][0])
                            letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
                            g.DrawText('{}'.format(pos[(col,row)][1]), letter_location, font='Courier 25')
                            ganar = False
                    if (sig == True) and (i < (len(lista)-1)):
                        i+=1
                if (total_letras == cont) and (ganar == True):
                    sg.Popup('FELICITACIONES!!! GANASTE!')



dic = []
reporte = []





>>>>>>> 029884f036ce91b6f844bb743d5e6d6addd30d52
tipografias = ('Arial', 'Courier', 'Comic', 'Fixedsys', 'Times', 'Verdana', 'Helvetica')
oficinas = ('Oficina 1', 'Oficina 2')
palabras = []

layout1 = [
    [sg.InputText(default_text="", key = 'ingreso')],
    [sg.Listbox([],size=(30, 6), key='lista' ),sg.Column([[sg.Button('Agregar')],[sg.Button('Eliminar')]])],
    [sg.Frame('Sustantivos', [[sg.Column([[sg.Spin([i for i in range(len([j for j in dic if j.getClase == 'sustantivo']))], initial_value=0, size= (15,1), key='cantSus')],[sg.ColorChooserButton('colorSus')]])]]), sg.Frame('Adjetivos', [[sg.Column([[sg.Spin([i for i in range(len([j for j in dic if j.getClase == 'adjetivo']))], initial_value=0, size= (15,1), key='cantAdj')],[sg.ColorChooserButton('colorAdj')]])]]), sg.Frame('Verbos', [[sg.Column([[sg.Spin([j for j in dic if j.getClase == 'verbo'], initial_value=0, size= (15,1), key = 'cantVerb')],[sg.ColorChooserButton('colorVerb')]])]])],
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
            dic, reporte = verificar_palabra(values['ingreso'], dic, reporte)
            print(dic[0].getPal())
            window.FindElement('lista').Update([i.getPal() for i in dic])
            window.FindElement('ingreso').Update('')
            window.FindElement('cantSus').Update(values=[i for i in range(len([j for j in dic if j.getClase() == 'sustantivo'])+1)])
            window.FindElement('cantAdj').Update(values=[i for i in range(len([j for j in dic if j.getClase() == 'adjetivo'])+1)])
            window.FindElement('cantVerb').Update(values=[i for i in range(len([j for j in dic if j.getClase() == 'verbo'])+1)])
    if event == 'Eliminar':
        if values['lista'] != []:
            for i in dic:
                if i.getPal() == values['lista'][0]:
                    dic.remove(i)
            window.FindElement('lista').Update([i.getPal() for i in dic])
            window.FindElement('cantSus').Update(values=[i for i in range(len([j for j in dic if j.getClase() == 'sustantivo'])+1)])
            window.FindElement('cantAdj').Update(values=[i for i in range(len([j for j in dic if j.getClase() == 'adjetivo'])+1)])
            window.FindElement('cantVerb').Update(values=[i for i in range(len([j for j in dic if j.getClase() == 'verbo'])+1)])
    if event == 'Generar reporte':
        texto = redactar_reporte(reporte)
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
<<<<<<< HEAD
        print(values['cantSus'])
        if values['cantSus'] != '0':
            i = 0
            while i < int(values['cantSus']):
                ran = random.randrange(len(dic))
                print(dic[ran].getClase())
                if dic[ran].getClase() == 'sustantivo':
                    if values['mayus'] == True:
                        dic[ran].aMayus()
                    else:
                        dic[ran].aMinus()
                    palabras.append(dic.pop(ran))
                    i+=1
        if values['cantAdj'] != '0':
            i = 0
            while i < int(values['cantAdj']):
                ran = random.randrange(len(dic))
                if dic[ran].getClase() == 'adjetivo':
                    if values['mayus'] == True:
                        dic[ran].aMayus()
                    else:
                        dic[ran].aMinus()
                    palabras.append(dic.pop(ran))
                    i+=1
        if values['cantVerb'] != '0':
            i = 0
            while i < int(values['cantVerb']):
                ran = random.randrange(len(dic))
                if dic[ran].getClase() == 'verbo':
                    if values['mayus'] == True:
                        dic[ran].aMayus()
                    else:
                        dic[ran].aMinus()
                    palabras.append(dic.pop(ran))
                    i+=1
        if values['colorSus'] == '':
            colorSus = '#ff0000'
        else:
            colorSus = values['colorSus']
        if values['colorAdj'] == '':
            colorAdj = '#00ff00'
        else:
            colorAdj = values['colorAdj']
        if values['colorVerb'] == '':
            colorVerb = '#0000ff'
        else:
            colorVerb = values['colorVerb']
        window.Close()
        juego(palabras, values['cantSus'], values['cantAdj'], values['cantVerb'], colorSus, colorAdj, colorVerb, values['mayus'], values['H'], values['ayDef'], values['ayListPal'], values['l&f'])
        break

>>>>>>> 029884f036ce91b6f844bb743d5e6d6addd30d52
        
        

