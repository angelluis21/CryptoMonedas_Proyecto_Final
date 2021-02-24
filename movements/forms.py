from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from movements import actions

monedas=('EUR', 'ETH', 'LTC', 'BNB', 'EOS', 'XLM', 'TRX', 'BTC', 'XRP', 'BCH', 'USDT', 'BSV', 'ADA')


def comprobarValor(form,field):
    if form.moneda_from.data != 'EUR':
        disponible = actions.totales()
        currency = form.moneda_from.data
        if disponible[currency] <=  field.data:
            raise ValidationError("Saldo insuficiente")

def comprobarMoneda(form,field):
    if form.moneda_from.data == form.moneda_to.data:
        raise ValidationError("¡ERROR! No se puede intercambiar entre el mismo típo de moneda")


class ClassForms(FlaskForm):
    moneda_from = SelectField('Moneda de cambio',validators=[DataRequired(), comprobarMoneda])
    moneda_to = SelectField('Moneda a cambiar', choices=monedas)
    cantidad_from = FloatField('Cantidad', validators=[DataRequired(message="Introduzca cantidad"),
    NumberRange (min=0.0000000001, max=10000000000, message="Cantidad errónea, introduzca una cantidad positiva o más pequeña"), comprobarValor])

    cantidad_to=FloatField('Cantidad')
    conversion=DecimalField("P.U:")


    total_invertido=FloatField("Euros totales invertidos:")
    valorActual=FloatField("Valor actual de todas sus inversiones:")
    valorNeto=FloatField("Resultado de su inversión:")

    calcular =SubmitField('Calcular')    
    submit = SubmitField('Aceptar')