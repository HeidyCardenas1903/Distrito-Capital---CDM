from flask import Flask, render_template, request, redirect,url_for,flash,session, make_response
from flask_login import login_required, login_manager
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
    '''Se establece la función para la ruta de inicio/home'''
    return render_template('modulos/index.html')#despues de que el usuario este ingresado se redirigira al index.html

'''Ruta para los manzanas'''
@app.route ('/manzanas')
def manzana():
    return render_template('modulos/manzanas.html')#Devolvera el template manzana.html

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