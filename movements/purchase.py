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


@app.route('/purchase', methods=['GET', 'POST'])
def transaccion():
    msg = []
    start=False
    form = ClassForms()
    fecha=actions.fecha()
    hora=actions.hora()
    try:
        dicResponse=actions.totales()
    except Exception as e:
        print("¡¡ ERROR !!: Acceso a base de datos-DBFILE:{} {}". format(type(e).__name__,e))
        msg.append("Error en acceso a base de datos. Consulte con el administrador.")
        return render_template("Purchase.html", form=form, msg=msg,start=False)
    coins=[]
    
    for item,valor in dicResponse.items():
        if valor> 0:
            coins.append(item)
    if not 'EUR' in coins:
        coins.append('EUR')
    
    form.moneda_from.choices=coins
    
    if request.method == 'POST': 
        if form.validate():
            if form.calcular.data ==True:
                try:
                    result= getConversion(url_api_crypto.format(form.cantidad_from.data,form.moneda_from.data,form.moneda_to.data,API_KEY))
                    moneda_from=result["data"]["symbol"]
                    cantidad_from=result["data"]["amount"]
                    moneda_to=(form.moneda_to.data)
                    cantidad_to=result["data"]["quote"][moneda_to]["price"]
                    conversion=float(cantidad_from)/float(cantidad_to)
                    form.cantidad_to.data = cantidad_to
                    form.conversion.data = conversion                   
                except Exception as e:
                    print("¡¡ ERROR !! de acceso al consultar la API:{} {}". format(type(e).__name__,e))
                    msg.append("Error en la consulta a la API. Consulte con el administrador.")
                    return render_template("Purchase.html", form=form, msg=msg,start=False)
                
                return render_template("Purchase.html", form=form,start=True)

            if form.submit.data:
                try:
                    actions.consulta ('INSERT INTO movimientos (fecha, hora, moneda_from, moneda_to, cantidad_from, cantidad_to, conversion) VALUES (?,?, ?, ?, ?,?,?);',
                            (
                                fecha,
                                hora,
                                form.moneda_from.data,
                                form.moneda_to.data,
                                float(form.cantidad_from.data),
                                round(float(form.cantidad_to.data),8),
                                round(float(form.conversion.data),8)
                            )
                                    )
                except Exception as e:
                    print("¡¡ ERROR !! de accerso al consultar la base de datos-DBFILE:{} {}". format(type(e).__name__,e))
                    msg.append("Error en el acceso a base de datos. Porfavor consulte con el administrador.")
                    return render_template("Purchase.html", form=form, msg=msg,start=False)

                return redirect(url_for('listadoMovimientos'))
            else:
                return render_template("Purchase.html", form=form) 
    return render_template("Purchase.html" , form=form, start=False )