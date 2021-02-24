from movements import app, actions
from movements.forms import ClassForms
from flask import render_template, request, url_for
import sqlite3
from config import *

DBFILE = app.config['DBFILE'] 

@app.route('/')
def listadoMovimientos():
    form = ClassForms()
    msg = []
    
    try:
        entry = actions.consulta('SELECT fecha, hora, moneda_from, cantidad_from, moneda_to, cantidad_to, conversion FROM movimientos;')
    except Exception as e:
        print("¡¡ ERROR !!: Acceso a base de datos-DBFILE:{} {}". format(type(e).__name__,e))
        msg.append("Error en acceso a base de datos. Consulte con el administrador.")

        return render_template("listMovements.html", form=form, msg=msg)

    return render_template("listMovements.html", datos=entry, form=form )