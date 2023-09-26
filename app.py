from flask import Flask, render_template, request, redirect,url_for,flash,session, make_response
from flask_login import login_required
from flask_mysqldb import MySQL
from reportlab.pdfgen import canvas
from modules.funciones import * 
import io

app = Flask(__name__)#Se especifica que este archivo es el que va a iniciar la webapp

'''Conexión a bd'''
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='manzanascuidado'
mysql=MySQL(app)

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
@app.route ('/municipios', methods=['GET','POST'])
def municipios():
    '''Se establece la función para la ruta para la seccion municipios'''
    if request.method == 'POST':
        cod = request.form['codmunicipio']
        name = request.form['nombres']

        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO municipios(cod_municipio,nombre_municipio) VALUES(%s,%s)',(cod,name))
        mysql.connection.commit()
        flash('Municipio Agregado')
        return redirect(url_for('municipios'))
    return render_template('modulos/municipios.html')#Devolvera el template municipios.html

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

def pdf_report(data):
    # Crear el PDF usando reportlab
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # Agregar contenido al PDF
    y = 700  # Posición inicial en y para el primer dato
    for row in data:
        x = 100  # Posición en x para el primer dato
        for value in row:
            p.drawString(x, y, str(value))
            x += 100  # Espaciado entre datos
        y -= 20  # Espaciado entre filas

    # Cerrar el PDF
    p.showPage()
    p.save()

    # Retornar el contenido del PDF
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


@app.route('/generar_pdf', methods=['POST'])
def generarpdf():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM municipios')
    data=cur.fetchall()

    pdf = pdf_report(data)

    response = make_response(pdf)
    response.headers['Content-Disposition'] = 'attachment; filename=reporte.pdf'
    response.mimetype = 'application/pdf'
    return response


if __name__=='__main__':
    #Se verifica que se este corriendo la aplicacion.
    app.run(debug=True)