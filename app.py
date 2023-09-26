from flask import Flask, render_template, request, redirect,url_for,flash,session
from flask_mysqldb import MySQL 
from modules.funciones import * 

app = Flask(__name__)#Se especifica que este archivo es el que va a iniciar la webapp

'''Conexión a bd'''

'''Settings'''
app.secret_key='mysecretkey'


'''Ruta para el index'''
@app.route('/')
def index():
    '''Se establece la función para la ruta del index'''
    return render_template('index.html')#Devolvera el template index.html


'''Ruta para el login'''
@app.route('/login')
def usuario():
    usuario = login()
    return usuario

'''Ruta para los municipios'''
@app.route ('/municipios')
def municipio():
    mun=municipios()
    return mun

'''Ruta para los manzanas'''
@app.route ('/manzanas')
def manzana():
    apple=manzanas()
    return apple

'''Ruta para los servicios'''
@app.route ('/servicios')
def servicio():
    service=servicios()
    return service

'''Ruta para los establecimientos'''
@app.route ('/establecimientos')
def establecimiento():
    est=establecimientos()
    return est

'''Ruta para las Cuidadoras'''
@app.route ('/mujeres')
def cuidadora():
    women=mujeres()
    return women


'''Ruta para la asignación'''
@app.route ('/asignacion')
def asignaciones():
    choose=asignacion()
    return choose

'''Ruta para los reportes'''
@app.route ('/reportes')
def reporte():
    report=reportes()
    return report



if __name__=='__main__':
    #Se verifica que se este corriendo la aplicacion.
    app.run(debug=True)