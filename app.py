from flask import Flask, render_template, request, redirect,url_for,flash,session
from flask_mysqldb import MySQL 

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

def login():
    '''Se establece la función para la ruta del login'''
    return render_template('login/login.html')#Devolvera el template login.html


if __name__=='__main__':
    #Se verifica que se este corriendo la aplicacion.
    app.run(debug=True)