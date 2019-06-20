import PySimpleGUI as sg
from pattern.es import parse, split
from pattern.web import Wiktionary

engine = Wiktionary(license=None, language='es')
dic = {'lista': [], 'sustantivo': [], 'adjetivo':[], 'verbo': [], 'reporte': [], 'def':{}}
sustantivos = []
adjetivos = []
verbos = []

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
    while True:
        try:
            filename = sg.PopupGetFile('Abrir', no_window = True, file_types = (("JSON Files", ".json")))
            if (filename != ''):
                with open(filename, "r") as infile:
                        aux = json.load(infile)
            break
        except PermissionError:
            sg.PopupOK('No tiene permisos para abrir este archivo')
    return [filename, aux]
    
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
    [sg.Checkbox('Look & feel'), sg.InputCombo(oficinas, size=(20, 1), key='ofi'), sg.Button('Abrir'), sg.Text('', key='dir')],
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
        window.FindElement('ofi').Update(values=arch[1].keys())
        window.FindElement('dir').Update(arch[0])
        
