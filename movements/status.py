from movements import app, actions
from movements.forms import ClassForms
from flask import render_template, request, url_for, redirect 
import sqlite3
from config import *
import requests

url_api_crypto = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"

def getConversion(url):
    response = requests.get(url)
    if response.status_code==200:
        data=response.json()
        return data


DBFILE = app.config['DBFILE'] 

@app.route('/status', methods=['GET', 'POST'])
def resumen():
    msg = []
    form = ClassForms()
    try:
        sumEurDB=actions.consulta('SELECT SUM(cantidad_from) AS total, moneda_from FROM movimientos WHERE moneda_from = "EUR" GROUP BY moneda_from;')
        sumEurDB=sumEurDB[0]['total']
        form.total_invertido.data =sumEurDB
        TotalEUR=actions.totales()["EUR"]
        valorActual=0
        dicResponse=actions.totales()
    except Exception as e:
        print("¡¡ ERROR !!: Posiblemente no se ha ejecutado ninguna operación con exito. Revise el acceso a la base de datos-DBFILE:{} {}". format(type(e).__name__,e))
        msg.append("Porfavor consulte con el administrador en caso de haber ejecutado alguna operación, por lo contrario vaya a la pantalla de inicio para empezar a invertir.")
        return render_template("status.html", form=form, msg=msg,start=False)

    for item,valor in dicResponse.items():
            if item != 'EUR':
                try:
                    result= getConversion(url_api_crypto.format(valor,item,"EUR",API_KEY))
                    sumaEUR=result["data"]["quote"]["EUR"]["price"]
                    valorActual+=float(sumaEUR)
                except Exception as e:
                    print("¡¡ ERROR !! de acceso a consulta con la API:{} {}". format(type(e).__name__,e))
                    msg.append("Error en la consulta a la API. Consulte con el administrador.")
                    return render_template("status.html", form=form, msg=msg,start=False)
            
    Total=round(valorActual+TotalEUR+sumEurDB,2)
    balance=round(Total-sumEurDB,2)

    form.valorActual.data = Total
    form.valorNeto.data= balance
    return render_template("status.html", form=form)