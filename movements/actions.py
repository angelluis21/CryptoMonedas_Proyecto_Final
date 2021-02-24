from movements import app
import sqlite3
import time
import datetime

DBFILE = app.config['DBFILE'] 


def consulta(query, params=()):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    c.execute(query, params)
    conn.commit()

    filas = c.fetchall()

    conn.close()

    if len(filas) == 0:
        return filas

    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0])

    listaDeDiccionarios = []

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames):
            d[columnName] = fila[ix]
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios

def hora():
    hora=time.strftime("%X")
    return hora

def fecha():
    fecha=datetime.date.today()
    return fecha

def listaMonedas(lista):
    listamonedas=[]
    for clave,valor in lista.items():
        if valor > 0:
            listamonedas.append(clave)
    if not 'EUR' in listamonedas:
        listamonedas.append('EUR')
    return listamonedas

def totales():
    diccionario = consulta('SELECT  moneda_from, cantidad_from, moneda_to, cantidad_to FROM movimientos;')
    dicResponse = {}
    for a in diccionario:
        claveFrom = a.get("moneda_from")
        cantidad_from = a.get("cantidad_from")
        claveTo = a.get("moneda_to")
        cantidad_to = a.get("cantidad_to")
        if dicResponse.get(claveTo) == None:
            dicResponse[claveTo]=cantidad_to
        else:
            dicResponse[claveTo]=cantidad_to+dicResponse[claveTo]
        if dicResponse.get(claveFrom) == None:
            dicResponse[claveFrom]=-cantidad_from
        else:
            dicResponse[claveFrom]=dicResponse[claveFrom]-cantidad_from
    return dicResponse
