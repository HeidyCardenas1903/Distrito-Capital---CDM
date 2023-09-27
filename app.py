from flask import Flask, render_template, request, redirect,url_for,flash,session, make_response
from flask_login import login_required, login_manager
from flask_mysqldb import MySQL
from reportlab.pdfgen import canvas
from modules.funciones import * 
import io
import xlwt 
import pymysql
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map



app = Flask(__name__)#Se especifica que este archivo es el que va a iniciar la webapp

'''Google Maps API'''
app.config['GOOGLEMAPS_KEY'] = "AIzaSyC-lmH6uemg3kFPtnjIO_l1YlKKDo5VYtY"

GoogleMaps(app)

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
    return render_template('modulos/login.html')#Devolvera el template index.html


'''Ruta para el login'''
@app.route('/login', methods=['GET','POST'])
def login():
    '''Función para el ingreso de usuarios'''
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['contrasenia']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios where usuarios.email=%s AND usuarios.contraseña=%s',(email,password))
        account = cur.fetchone()

        if account:
            session['Logueado']=True


            return redirect(url_for('inicio'))#si el usuario ingresa correctamente lo redireccionara al home

        
        else:
            flash('Datos incorrectos')#Si no, le saldra un mensaje de validacion y lo redirigirá al login de nuevo 
            return render_template('modulos/login.html')
    return render_template('modulos/login.html')#Devolvera el template login.html

@app.route('/logout')
def logout():
    # Elimina la sesión del usuario
    session.clear()
    flash('Has cerrado sesion exitosamente', 'success')
    return redirect(url_for('login'))  # Redirige a la página de inicio de sesión

'''Ruta para los municipios'''
@app.route ('/municipios', methods=['GET','POST'])
def municipios():
    '''Se establece la función para la ruta para la seccion municipios'''
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM municipios')
    info=cur.fetchall()

    if request.method == 'POST':
        cod = request.form['codmunicipio']
        name = request.form['nombres']

        cur.execute('SELECT * FROM municipios WHERE cod_municipio=%s',[cod,])#Se verifica que el municipio no haya sido previamente ingresado
        data=cur.fetchone()

        if data:
            flash('Municipio ya Registrado')
            return redirect(url_for('municipios'))#Si el municipio se encuentra ya resgistrao se habilita el mensaje de aviso y se redirije al formulario

        else:
            cur.execute('INSERT INTO municipios(cod_municipio,nombre_municipio) VALUES(%s,%s)',(cod,name))
            mysql.connection.commit()
            flash('Municipio Agregado')
            return redirect(url_for('municipios'))
    return render_template('modulos/municipios.html', municipios=info)#Devolvera el template municipios.html

@app.route('/municipio/borrar/<string:cod_municipio>', methods=['GET','POST'])
def borrarmunicipio(cod_municipio):
    '''Funcion encargada de borrar registros de la tabla municipios'''
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM municipios WHERE cod_municipio={0}'.format(cod_municipio))
    mysql.connection.commit()
    flash('Registro Eliminado')
    return redirect(url_for('municipios'))

'''Ruta de inicio'''
@app.route ('/index')
def inicio():
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': 37.4419,
             'lng': -122.1419,
             'infobox': "<b>Hello World</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
             'lat': 37.4300,
             'lng': -122.1400,
             'infobox': "<b>Hello World from other place</b>"
          }
        ]
    )
    return render_template('modulos/index.html',mymap=mymap, sndmap=sndmap)#despues de que el usuario este ingresado se redirigira al index.html

'''Ruta para los manzanas'''
@app.route ('/manzanas',methods=['GET','POST'])
def manzana():
    '''Se establece la función para la ruta para la seccion municipios'''
    cur=mysql.connection.cursor()
    cur.execute('SELECT cod_manzana,nombre_municipio,nombre_manzana,localidad,direccion_manzana,nombre_servicio FROM manzanas,municipios,servicios,appleservice WHERE manzanas.cod_municipio=municipios.cod_municipio AND manzanas.cod_manzana=appleservice.copy_codmanzana AND servicios.cod_servicio=appleservice.copy_codservice')
    info=cur.fetchall()
    print(info)

    if request.method == 'POST':
        cod = request.form['codmanzana']
        name = request.form['nombres']
        cod2 = request.form['codmunicipio']
        localidad = request.form['localidad']
        direccion = request.form['direccion']
        codserv=request.form['servicioprest']

        
        cur.execute('SELECT * FROM manzanas WHERE cod_manzana=%s',[cod,])#Se verifica que el municipio no haya sido previamente ingresado
        data=cur.fetchone()

        if data:
            flash('Manzana ya registrada')
            return redirect(url_for('manzana'))#Si la manzana se encuentra ya resgistrao se habilita el mensaje de aviso y se redirije al formulario


        else:
            cur.execute('INSERT INTO manzanas(cod_manzana,cod_municipio,nombre_manzana,localidad,direccion_manzana) VALUES(%s,%s,%s,%s,%s)',(cod,cod2,name,localidad,direccion))
            cur.execute('INSERT INTO appleservice(copy_codmanzana,copy_codservice) VALUES(%s,%s)',(cod,codserv))
            mysql.connection.commit()
            flash('Manzana Agregada')
            return redirect(url_for('manzana'))
    return render_template('modulos/manzanas.html', manzanas=info)#Devolvera el template manzana.html

@app.route('/manzana/borrar/<string:cod_manzana>', methods=['GET','POST'])
def borrarmanzana(cod_manzana):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM appleservice WHERE copy_codmanzana={0}'.format(cod_manzana))
    mysql.connection.commit()
    cur.execute('DELETE FROM manzanas WHERE cod_manzana={0}'.format(cod_manzana))
    mysql.connection.commit()
    flash('Registro Eliminado')
    return redirect(url_for('manzana'))

'''Ruta para los servicios'''
@app.route ('/servicios', methods=['GET','POST'])
def servicios():
    '''Se establece la función para la ruta para la seccion servicios'''
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM servicios')
    info=cur.fetchall()

    if request.method == 'POST':
        cod = request.form['codservicio']
        name = request.form['nombres']
        description = request.form['descripcion']

        cur.execute('SELECT * FROM servicios WHERE cod_servicio=%s',[cod,])#Se verifica que el servicio no haya sido previamente ingresado
        data=cur.fetchone()

        if data:
            flash('Servicio ya Registrado')
            return redirect(url_for('servicios'))#Si el servicio se encuentra ya resgistrao se habilita el mensaje de aviso y se redirije al formulario

        else:
            cur.execute('INSERT INTO servicios(cod_servicio,nombre_servicio,descripcion) VALUES(%s,%s,%s)',(cod,name,description))
            mysql.connection.commit()
            flash('Servicio Agregado')
            return redirect(url_for('servicios'))

    return render_template('modulos/servicios.html', servicios=info)#Devolvera el template servicios.html ubicado en la carpeta templates/modulos

@app.route('/servicio/borrar/<string:cod_servicio>', methods=['GET','POST'])
def borrarservicio(cod_servicio):
    '''Funcion encargada de borrar registros de la tabla municipios'''
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM servicios WHERE cod_servicio={0}'.format(cod_servicio))
    mysql.connection.commit()
    flash('Registro Eliminado')
    return redirect(url_for('servicios'))

'''Ruta para los establecimientos'''
@app.route ('/establecimientos', methods=['GET','POST'])
def establecimientos():
    '''Se establece la función para la ruta para la seccion establecimientos'''
    cur=mysql.connection.cursor()
    cur.execute('SELECT cod_establecimiento,nombre_establecimiento,responsable,direccion_establecimiento,nombre_servicio FROM establecimiento,servicios WHERE establecimiento.cod_servicio=servicios.cod_servicio')
    info=cur.fetchall()
    print(info)

    if request.method == 'POST':
        cod = request.form['codestablecimiento']
        name = request.form['nombres']
        responsable = request.form['responsable']
        direccion = request.form['direccion']
        service= request.form['service']

        cur.execute('SELECT * FROM establecimiento WHERE cod_establecimiento=%s',[cod,])#Se verifica que el establecimiento no haya sido previamente ingresado
        data=cur.fetchone()

        if data:
            flash('Establecimiento ya registrado')
            return redirect(url_for('establecimientos'))#Si el servicio se encuentra ya resgistrao se habilita el mensaje de aviso y se redirije al formulario

        else:
            cur.execute('INSERT INTO establecimiento(cod_establecimiento,cod_servicio,nombre_establecimiento,responsable,direccion_establecimiento) VALUES(%s,%s,%s,%s,%s)',(cod,service,name,responsable,direccion))
            mysql.connection.commit()
            flash('Establecimiento Agregado')
            return redirect(url_for('establecimientos'))

    return render_template('modulos/establecimientos.html',establecimiento=info)#Devolvera el template establecimientos.html

@app.route('/establecimiento/borrar/<string:cod_establecimiento>', methods=['GET','POST'])
def borrarestablecimiento(cod_establecimiento):
    '''Funcion encargada de borrar registros de la tabla establecimientos'''
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM establecimiento WHERE cod_establecimiento={0}'.format(cod_establecimiento))
    mysql.connection.commit()
    flash('Registro Eliminado')
    return redirect(url_for('establecimientos'))

'''Ruta para las Cuidadoras'''
@app.route ('/mujeres', methods=['GET','POST'])
def cuidadora():
    '''Se establece la función para la ruta para la seccion Cuidadoras'''
    cur=mysql.connection.cursor()
    cur.execute('SELECT documento,nombre_servicio,tipoDocumento,nombres_mujer,apellidos_mujer,telefono,correo,ciudad,direccion_mujer,ocupacion FROM mujeres,servicios WHERE mujeres.cod_servicio=servicios.cod_servicio')
    info=cur.fetchall()#Esta seleccion va a mostrar los campos que esten existentes en la bd de la tabla

    if request.method == 'POST':
        tipodoc = request.form['tipodoc']
        doc = request.form['documento']
        name = request.form['nombres']
        lastname = request.form['apellidos']
        tel = request.form['telefono']
        email = request.form['correo']
        city = request.form['ciudad']
        address = request.form['direccion']
        ocupacion = request.form['ocupacion']
        servicioint = request.form['servicioint']
        
     
        cur.execute('SELECT * FROM mujeres WHERE documento=%s',[doc,])#Se verifica que la mujer no haya sido previamente ingresada
        data=cur.fetchone()

        if data:
            flash('Cuidadora ya Registrada')
            return redirect(url_for('cuidadora'))#Si la mujer se encuentra ya resgistrada se habilita el mensaje de aviso y se redirije al formulario

        else:
            cur.execute('SELECT * FROM mujeres WHERE correo=%s',[email,])#Se verifica que el email no haya sido registrado anteriormente
            data=cur.fetchone()

            if data:
                flash('Email ya Registrado')
                return redirect(url_for('cuidadora'))#Si el email se encuentra ya resgistrado se habilita el mensaje de aviso y se redirije al formulario
            else:
                cur.execute('INSERT INTO mujeres(documento,cod_servicio,tipoDocumento,nombres_mujer,apellidos_mujer,telefono,correo,ciudad,direccion_mujer,ocupacion) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(doc,servicioint,tipodoc,name,lastname,tel,email,city,address,ocupacion))
                mysql.connection.commit()
                flash('Cuidadora Agregada Satisfactoriamente')
        return redirect(url_for('cuidadora'))#SI el registro se completa satisfactoriamente se habilita el mensaje y se redirige al formulario
    
    return render_template('modulos/mujeres.html', mujeres=info)#Devolvera el template mujeres.html

@app.route('/mujer/borrar/<string:documento>', methods=['GET','POST'])
def borrarmujer(documento):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM mujeres WHERE documento={0}'.format(documento))
    mysql.connection.commit()
    flash('Registro Eliminado')
    return redirect(url_for('cuidadora'))


'''Ruta para la asignación'''
@app.route ('/asignacion')
def asignaciones():
    choose=asignacion()
    return choose

@app.route('/establecimiento/borrar/<string:cod_establecimiento>', methods=['GET','POST'])
def borrarasignacion(cod_establecimiento):
    '''Funcion encargada de borrar registros de la tabla municipios'''
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM establecimiento WHERE cod_establecimiento={0}'.format(cod_establecimiento))
    mysql.connection.commit()
    flash('Registro Eliminado')
    return redirect(url_for('establecimientos'))

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


# @app.route('/generar_xlx')
# def generar_xlx():
#     conn = mysql.connect()
#     cursor= conn.cursor(pymysql.cursors.DictCursor)

#     cursor.execute('SELECT * FROM municipios')
#     result = cursor.fetchall()

#     output =io.BytesIO()
#     workbook = xlwt.Workbook()
#     sh = workbook.add_sheet('Reporte')