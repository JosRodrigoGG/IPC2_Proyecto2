import os
import webbrowser
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

import graphviz as graphviz

import os.path as path
from xml.dom import minidom

from bin.LineaProduccion import LineaProduccion
from bin.Lista import Lista
from bin.Maquina import Maquina
from bin.Producto import Producto
from bin.Simulacion import Simulacion

LISTA_MAQUINA = Lista()
LISTA_SIMULACION = Lista()
LISTA_COMBO = []


def generarHTML():
    if str(comboBoxReporte.get()) != "":
        nombreProducto = str(comboBoxReporte.get())
        maquina = Maquina(0)
        producto = Producto("")

        aux1 = LISTA_MAQUINA.primero
        while aux1:
            aux2 = aux1.dato.getProductos().primero
            while aux2:
                if aux2.dato.getNombre() == nombreProducto:
                    maquina = aux1.dato
                    producto = aux2.dato
                aux2 = aux2.siguiente
                if aux2 == aux1.dato.getProductos().primero:
                    break
            aux1 = aux1.siguiente
            if aux1 == LISTA_MAQUINA.primero:
                break

        COMPONENTES = componentesNecesarios(producto.getLista())

        COLUMNS = ["TIEMPO"]
        contador = 0
        while contador < maquina.getCantidadLineasProduccion():
            COLUMNS.append(str("LINEA " + str(contador + 1)))
            contador += 1

        listaTreeView = analizarProduccion(analizarEnsamble(producto.getLista(), maquina.getCantidadLineasProduccion()),
                                           maquina.getCantidadLineasProduccion())

        tiempo = 0
        for data in listaTreeView:
            tiempo = int(data[0])

        guardar = filedialog.asksaveasfilename(initialdir="/", title="Guardar archivo de salida",
                                               defaultextension=".html",
                                               filetypes=(("HTML", "*.html"),
                                                          ("txt", "*.txt"),
                                                          ("All files", "*")))
        archivo = open(guardar, "w")

        contenido = ("" +
                     "<!DOCTYPE html>\n" +
                     "<html lang='en'>\n" +
                     "<head>\n" +
                     "\t<meta charset='UTF-8'>\n" +
                     "\t<title>\nSimulación</title>\n" +
                     "\t<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css'>\n" +
                     "\t<link href='https://fonts.googleapis.com/icon?family=Material+Icons' rel='stylesheet'>\n" +
                     "</head>\n" +
                     "<body>\n" +
                     "<div class='container'>\n" +
                     "\t<div class='row'>\n" +
                     "\t\t<div class='col s12 center-align'>\n" +
                     "\t\t\t<h2>\nREPORTE</h2>\n" +
                     "\t\t\t<h6>\n<b>\n<i>\nSIMULACION</i>\n</b>\n</h6>\n" +
                     "\t\t</div>\n" +
                     "\t\t<div class='col s5 center-align'>\n" +
                     "\t\t\t<div class='card-panel'>\n" +
                     "\t\t\t\t<h6>\n" + str(producto.getNombre()) + "</h6>\n" +
                     "\t\t\t</div>\n" +
                     "\t\t\t<br>\n" +
                     "\t\t\t<h6>\n<b>\nComponentes necesarios</b>\n</h6>\n" +
                     "\t\t\t<br>\n" +
                     "\t\t\t<div class='row'>\n" +
                     "\t\t\t\t<div class='col s8 offset-s2'>\n" +
                     "\t\t\t\t\t<ul class='collection'>\n")

        for data in COMPONENTES:
            contenido = (contenido +
                         "\t\t\t\t\t\t<li class='collection-item'>\n" + str(data) + "</li>\n")

        contenido = (contenido +
                     "\t\t\t\t\t</ul>\n" +
                     "\t\t\t\t</div>\n" +
                     "\t\t\t</div>\n" +
                     "\t\t</div>\n" +
                     "\t\t<div class='col s1'>\n" +
                     "\t\t\t<br>\n" +
                     "\t\t</div>\n" +
                     "\t\t<div class='col s6 center-align'>\n" +
                     "\t\t\t<table class='striped centered'>\n" +
                     "\t\t\t\t<h6>\n<b>\nEnsamblado de producto</b>\n</h6>\n" +
                     "\t\t\t\t<br>\n" +
                     "\t\t\t\t<thead>\n" +
                     "\t\t\t\t<tr>\n")

        for data in COLUMNS:
            contenido = (contenido +
                         "\t\t\t\t\t<th>\n" + str(data) + "</th>\n")

        contenido = (contenido +
                     "\t\t\t\t</tr>\n" +
                     "\t\t\t\t</thead>\n" +
                     "\t\t\t\t<tbody>\n")

        for data1 in listaTreeView:
            contenido = (contenido + "\t\t\t\t<tr>\n")
            for data2 in data1:
                contenido = (contenido + "\t\t\t\t\t<td>\n" + str(data2) + "</td>\n")
            contenido = (contenido + "\t\t\t\t</tr>\n")

        contenido = (contenido +
                     "\t\t\t\t</tbody>\n" +
                     "\t\t\t</table>\n" +
                     "\t\t\t<br>\n" +
                     "\t\t\t<div class='row'>\n" +
                     "\t\t\t\t<div class='col s4 offset-s4 center-align'>\n" +
                     "\t\t\t\t\t<div class='card-panel'>\n" +
                     "\t\t\t\t\t\t<h6>TIEMPO: " + str(tiempo) + " segundos</h6>\n" +
                     "\t\t\t\t\t</div>\n" +
                     "\t\t\t\t</div>\n" +
                     "\t\t\t</div>\n" +
                     "\t\t</div>\n" +
                     "\t</div>\n" +
                     "</div>\n" +
                     "<script src='https://code.jquery.com/jquery-3.6.0.min.js'>\n</script>\n" +
                     "<script src='https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js'>\n</script>\n" +
                     "</body>\n" +
                     "</html>\n")

        archivo.write(contenido)
        archivo.close()
        webbrowser.open_new_tab(guardar)


def generarReporteCola():
    if str(comboBoxReporte.get()) != "":
        nombreProducto = str(comboBoxReporte.get())
        producto = Producto("")

        aux1 = LISTA_MAQUINA.primero
        while aux1:
            aux2 = aux1.dato.getProductos().primero
            while aux2:
                if aux2.dato.getNombre() == nombreProducto:
                    producto = aux2.dato
                aux2 = aux2.siguiente
                if aux2 == aux1.dato.getProductos().primero:
                    break
            aux1 = aux1.siguiente
            if aux1 == LISTA_MAQUINA.primero:
                break

        guardar = filedialog.askdirectory()

        if guardar != "":
            os.chdir(guardar)

            grafico = graphviz.Digraph('G', filename=str(producto.getNombre()), format="png",
                                       directory=str(os.getcwd()))
            grafico.attr(rankdir="LR")
            grafico.attr("node", shape="circle")

            PROCEDIMIENTO = []
            aux = producto.getLista().primero
            while aux:
                PROCEDIMIENTO.append(aux.dato)
                aux = aux.siguiente
                if aux == producto.getLista().primero:
                    break

            for data in PROCEDIMIENTO:
                grafico.node(data)

            cont = 0
            while (cont + 1) < len(PROCEDIMIENTO):
                grafico.edge(PROCEDIMIENTO[cont], PROCEDIMIENTO[cont + 1])
                cont += 1

            grafico.view()


def archivoMaquina():
    ruta = filedialog.askopenfilename(initialdir="/",
                                      title="Seleccione archivo", filetypes=(("xml files", "*.xml"),
                                                                             ("all files", "*.*")))
    if path.isfile(ruta):
        archivo_xml = minidom.parse(ruta)
        items = archivo_xml.getElementsByTagName("Maquina")

        for temp in items:
            maquina = Maquina(int(temp.getElementsByTagName("CantidadLineasProduccion")[0].childNodes[0].data))

            listadoLineasProduccion = temp.getElementsByTagName("ListadoLineasProduccion")[0].getElementsByTagName(
                "LineaProduccion")
            for lista in listadoLineasProduccion:
                numero = int(lista.getElementsByTagName("Numero")[0].childNodes[0].data)
                componentes = int(lista.getElementsByTagName("CantidadComponentes")[0].childNodes[0].data)
                tiempo = int(lista.getElementsByTagName("TiempoEnsamblaje")[0].childNodes[0].data)
                maquina.agregarLineasProduccion(LineaProduccion(numero, componentes, tiempo))

            listadoProductos = temp.getElementsByTagName("ListadoProductos")[0].getElementsByTagName(
                "Producto")
            for lista in listadoProductos:
                nombre = str(
                    lista.getElementsByTagName("nombre")[0].childNodes[0].data.replace('\n', "").replace(" ", ""))
                listaElaboracion = lista.getElementsByTagName("elaboracion")[0].childNodes[0].data.split()
                producto = Producto(nombre.replace('\t',""))

                for elaboracion in listaElaboracion:
                    producto.agregarElaboracion(elaboracion)
                maquina.agregarProducto(producto)

            LISTA_MAQUINA.agregar(maquina)


def archivoSimulacion():
    ruta = filedialog.askopenfilename(initialdir="/",
                                      title="Seleccione archivo", filetypes=(("xml files", "*.xml"),
                                                                             ("all files", "*.*")))

    if path.isfile(ruta):
        archivo_xml = minidom.parse(ruta)
        items = archivo_xml.getElementsByTagName("Simulacion")

        for temp in items:
            simulacion = Simulacion(str(temp.getElementsByTagName("Nombre")[0].childNodes[0].data.replace(" ", "")))

            listadoProductos = temp.getElementsByTagName("ListadoProductos")[0].getElementsByTagName(
                "Producto")
            for lista in listadoProductos:
                simulacion.agregarProductos(str(lista.childNodes[0].data.replace(" ", "")).replace('\n', ""))

            LISTA_SIMULACION.agregar(simulacion)

    LISTA_COMBO = []
    aux1 = LISTA_SIMULACION.primero
    while aux1:
        aux2 = aux1.dato.getListaProductos().primero
        while aux2:
            LISTA_COMBO.append(aux2.dato)
            aux2 = aux2.siguiente
            if aux2 == aux1.dato.getListaProductos().primero:
                break
        aux1 = aux1.siguiente
        if aux1 == LISTA_SIMULACION.primero:
            break

    comboBox['values'] = LISTA_COMBO
    comboBoxReporte['values'] = LISTA_COMBO


def iniciarSimulacion():
    if str(comboBox.get()) != "":
        nombreProducto = str(comboBox.get())
        maquina = Maquina(0)
        producto = Producto("")

        aux1 = LISTA_MAQUINA.primero
        while aux1:
            aux2 = aux1.dato.getProductos().primero
            while aux2:
                print(str(aux2.dato.getNombre()).replace(" ",""))
                if aux2.dato.getNombre() == nombreProducto:
                    print(nombreProducto)
                    maquina = aux1.dato
                    producto = aux2.dato
                aux2 = aux2.siguiente
                if aux2 == aux1.dato.getProductos().primero:
                    break
            aux1 = aux1.siguiente
            if aux1 == LISTA_MAQUINA.primero:
                break

        listBox.delete(0, END)
        COMPONENTES = componentesNecesarios(producto.getLista())
        for data in COMPONENTES:
            listBox.insert(1, str(data))

        COLUMNS = ["TIEMPO"]
        contador = 0
        while contador < maquina.getCantidadLineasProduccion():
            COLUMNS.append(str("LINEA " + str(contador + 1)))
            contador += 1

        treeView['columns'] = COLUMNS
        treeView.column("#0", width=0, stretch=NO)
        treeView.heading("#0", text="")

        listaTreeView = analizarProduccion(analizarEnsamble(producto.getLista(), maquina.getCantidadLineasProduccion()),
                                           maquina.getCantidadLineasProduccion())

        for temp in COLUMNS:
            treeView.column(str(temp), width=100)
            treeView.heading(str(temp), text=str(temp))

        for data in treeView.get_children():
            treeView.delete(data)

        count = 0
        tiempo = 0
        for data in listaTreeView:
            tiempo = int(data[0])
            treeView.insert(parent="", index="end", iid=count, values=(data))
            count += 1

        labelTiempo['text'] = "TIEMPO: " + str(tiempo) + " segundos"


def componentesNecesarios(lista):
    COMPONENETES = []

    aux = lista.primero
    while aux:
        COMPONENETES.append(str("COMPONENTE " + str(aux.dato)[1:-1].replace("pC", " ").split(" ")[1]))
        aux = aux.siguiente
        if aux == lista.primero:
            break

    return COMPONENETES


def analizarProduccion(lista, numeroLineas):
    CONTENIDO = []
    CONTENIDO_TEMP = []

    linea = 1
    while True:
        temp = []
        cont1 = 0
        while cont1 < len(lista):
            if int(lista[cont1][0]) == int(linea):
                temp.append([lista[cont1][1], lista[cont1][2]])
            cont1 += 1
        CONTENIDO_TEMP.append(temp)
        linea += 1
        if linea > numeroLineas:
            break

    cont1 = 0
    filas = 0
    while cont1 < len(CONTENIDO_TEMP):
        if filas < len(CONTENIDO_TEMP[cont1]):
            filas = len(CONTENIDO_TEMP[cont1])
        cont1 += 1

    temp = 0
    while temp < filas:
        CONTENIDO.append([])
        temp += 1

    cont1 = 0
    while cont1 < len(CONTENIDO_TEMP):
        cont2 = 0
        while cont2 < len(CONTENIDO_TEMP[cont1]):
            if len(CONTENIDO[0]) == 0:
                CONTENIDO[cont2] = CONTENIDO_TEMP[cont1][cont2]
            else:
                if len(CONTENIDO[cont2]) == 0:
                    CONTENIDO[cont2] = CONTENIDO_TEMP[cont1][cont2]
                else:
                    if int(CONTENIDO[cont2][0]) == int(CONTENIDO_TEMP[cont1][cont2][0]):
                        CONTENIDO[cont2].append(CONTENIDO_TEMP[cont1][cont2][1])
            cont2 += 1
        cont1 += 1

    cont1 = 0
    while cont1 < len(CONTENIDO):
        if len(CONTENIDO[cont1]) != (numeroLineas + 1):
            CONTENIDO[cont1].append("No hace nada")
        cont1 += 1

    return CONTENIDO


def analizarEnsamble(lista, numeroLineas):
    PRODUCCION = []
    tempLista = []

    aux = lista.primero
    while aux:
        tempLista.append(str(aux.dato)[1:-1].replace("pC", " ").split(" "))
        aux = aux.siguiente
        if aux == lista.primero:
            break

    contador = 0
    lineas = 1
    numeroComponente = 0
    segundos = 0

    while True:
        while contador < len(tempLista):
            if int(lineas) == int(tempLista[contador][0]):
                if int(tempLista[contador][1]) > numeroComponente:
                    while numeroComponente < int(tempLista[contador][1]):
                        segundos += 1
                        numeroComponente += 1
                        PRODUCCION.append([str(lineas), str(segundos), "Mover a C" + str(numeroComponente)])
                    segundos += 1
                    PRODUCCION.append([str(lineas), str(segundos), "ENSAMBLAR C" + str(numeroComponente)])
                elif int(tempLista[contador][1]) < numeroComponente:
                    while numeroComponente > int(tempLista[contador][1]):
                        segundos += 1
                        numeroComponente -= 1
                        PRODUCCION.append([str(lineas), str(segundos), "Mover a C" + str(numeroComponente)])
                    segundos += 1
                    PRODUCCION.append([str(lineas), str(segundos), "ENSAMBLAR C" + str(numeroComponente)])
                elif int(tempLista[contador][1]) == numeroComponente:
                    segundos += 1
                    PRODUCCION.append([str(lineas), str(segundos), "ENSAMBLAR C" + str(numeroComponente)])
            contador += 1
        contador = 0
        numeroComponente = 0
        segundos = 0
        lineas += 1
        if lineas > numeroLineas:
            break

    return PRODUCCION


root = Tk()
root.geometry("650x350")
root.title("Simulador")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

tabControl = Notebook(root)
tabControl.pack(pady=15)

tab1 = Frame(tabControl, width=600, height=500)
tab2 = Frame(tabControl, width=600, height=500)
tab3 = Frame(tabControl, width=600, height=500)
tab4 = Frame(tabControl, width=600, height=500)

tabControl.add(tab1, text="Simulacion")
tabControl.add(tab2, text="Archivo")
tabControl.add(tab3, text="Reporte")

Label(tab2, text="CARGAR ARCHIVOS", font=("Helvetica", 12)).grid(row=0, column=0, columnspan=7, pady=5)
Label(tab2, text="CARGAR MÁQUINA", font=("Helvetica", 10)).grid(row=1, column=0, columnspan=3)
Label(tab2, text="Seleccione un archivo .xml", font=("Helvetica", 9, "italic"), compound=LEFT).grid(row=2, column=0,
                                                                                                    columnspan=3,
                                                                                                    pady=5)
Button(tab2, text="CARGAR", command=archivoMaquina).grid(row=3, column=1)
Label(tab2, text="CARGAR SIMULACIÓN", font=("Helvetica", 10)).grid(row=1, column=4, columnspan=3)
Label(tab2, text="Seleccione un archivo .xml", font=("Helvetica", 9, "italic"), compound=LEFT).grid(row=2, column=4,
                                                                                                    columnspan=3,
                                                                                                    pady=5)
Button(tab2, text="CARGAR", command=archivoSimulacion).grid(row=3, column=5)

Label(tab1, text="SIMULACION", font=("Helvetica", 12)).grid(row=0, column=0, columnspan=3)
Label(tab1, text="Seleccione un producto para iniciar la simulación", font=("Helvetica", 9, "italic")).grid(row=1,
                                                                                                            column=0,
                                                                                                            columnspan=3)
comboBox = Combobox(tab1, state="readonly")
comboBox['values'] = LISTA_COMBO
comboBox.grid(row=2, column=0, columnspan=2)
Button(tab1, text="INICIAR", command=iniciarSimulacion).grid(row=2, column=2)
Label(tab1, text="Componentes necesarios", font=("Helvetica", 10,)).grid(row=4, column=0, columnspan=3)
listBox = Listbox(tab1)
listBox.grid(row=5, column=1)

listaTreeView = []

labelTiempo = Label(tab1, text="TIEMPO:")
labelTiempo.grid(row=1, column=3)

treeView = Treeview(tab1)
treeView['columns'] = ()

treeView.grid(row=2, column=3, rowspan=5, columnspan=2)

Label(tab3, text="GENERAR REPORTES", font=("Helvetica", 12)).grid(row=0, column=0, columnspan=7, pady=5)
comboBoxReporte = Combobox(tab3, state="readonly")
comboBoxReporte['values'] = LISTA_COMBO
comboBoxReporte.grid(row=1, column=0, columnspan=7)

Label(tab3, text="REPORTE HTML", font=("Helvetica", 10)).grid(row=2, column=0, columnspan=3)
Label(tab3, text="Guardar archivo .html", font=("Helvetica", 9, "italic"), compound=LEFT).grid(row=3, column=0,
                                                                                               columnspan=3,
                                                                                               pady=5)
Button(tab3, text="GENERAR", command=generarHTML).grid(row=4, column=1)
Label(tab3, text="REPORTE COLA", font=("Helvetica", 10)).grid(row=2, column=4, columnspan=3)
Label(tab3, text="Guardar reporte de colas .png", font=("Helvetica", 9, "italic"), compound=LEFT).grid(row=3, column=4,
                                                                                                       columnspan=3,
                                                                                                       pady=5)
Button(tab3, text="GENERAR", command=generarReporteCola).grid(row=4, column=5)

Style(root).configure("TNotebook", tabposition='n')
root.mainloop()
