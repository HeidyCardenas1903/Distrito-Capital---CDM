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



'''Ruta para de los index'''
@app.route('/')
def index():
    '''Se establece la función para la ruta del index'''
    return render_template('login.html')#Devolvera el template index.html
@app.route('/inicioMujer')
def inicioMujer():
    '''Se establece la función para la ruta del index'''
    return render_template('Mujer/indexMujer.html')#Devolvera el template indexMujer.html
@app.route ('/index')
def inicio():
    return render_template('Admin/index.html')#despues de que el usuario este ingresado se redirigira al index.html


'''Ruta para el login'''
@app.route('/login', methods=['GET','POST'])
def login():
    '''Función para el ingreso de usuarios'''
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['contrasenia']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM mujeres where mujeres.correo=%s AND mujeres.contraseña=%s',(email,password))
        account = cur.fetchone()

        if account:
            session['Logueado']=True


            return redirect(url_for('inicioMujer'))#si el usuario ingresa correctamente lo redireccionara al index de las mujeres
        else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM usuarios where usuarios.email=%s AND usuarios.contraseña=%s',(email,password))
            admin = cur.fetchone()#si el usuario ingresa correctamente lo redireccionara al index del admin

            if admin:
                session['Logueado']=True
                flash('Bienvenido usuario administrador')
                return redirect(url_for('inicio'))#si el usuario ingresa correctamente lo redireccionara al home
            else:
                flash('Datos incorrectos')#Si no, le saldra un mensaje de validacion y lo redirigirá al login de nuevo 
                return render_template('login.html')
    return render_template('login.html')
'''Ruta para el Logout'''
@app.route('/logout')
def logout():
    # Elimina la sesión del usuario
    session.clear()
    flash('Has cerrado sesion exitosamente', 'success')
    return redirect(url_for('login'))  # Redirige a la página de inicio de sesión


'''Restablecer contraseña'''
@app.route('/restablecer', methods=('GET','POST'))
def restablecer():

    if request.method == 'POST':
        email = request.form['email']
        documento=request.form['documento']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM mujeres where documento=%s AND mujeres.correo=%s',(documento,email))
        account = cur.fetchone()

        if account:
            return redirect(url_for('cambiocontra'))
        else:
            flash('Email no registrado')
            return redirect(url_for('login'))
    return render_template('restablecer.html')

@app.route('/cambiocontra',methods=('GET','POST'))
def cambiocontra():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM mujeres')
    info=cur.fetchall()
    cur.close()
    return render_template('cambiocontra.html',mujeres=info[0])

@app.route('/updatecontra/<documento>',methods=('GET','POST'))
def updatecontra(documento):
    if request.method=='POST':
        contra = request.form['contra']

        cur = mysql.connection.cursor()
        cur.execute('UPDATE mujeres SET contraseña=%s WHERE documento=%s',(contra,documento))
        mysql.connection.commit()
        flash('Contraseña Actualizada')
        return redirect(url_for('login'))



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
    return render_template('admin/municipios.html', municipios=info)#Devolvera el template municipios.html
'''Ruta encargada de capturar la primary key de los registros de municipios'''
@app.route('/municipio/edit/<cod_municipio>', methods=['POST', 'GET'])
def get_municipios(cod_municipio):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM municipios')
    info=cur.fetchall()
    cur.close()
    return render_template('edicion/editmunicipios.html',municipios=info[0])
'''Ruta encargada de editar registros de municipios'''
@app.route('/municipio/update/<cod_municipio>',methods=['GET','POST'])
def update_municipios(cod_municipio):

    if request.method=='POST':
        cod = request.form['codmunicipio']
        name = request.form['nombres']

        cur = mysql.connection.cursor()
        cur.execute('UPDATE municipios SET nombre_municipio=%s WHERE cod_municipio=%s',(name,cod))
        mysql.connection.commit()
        flash('Municipio Actualizado')
        return redirect(url_for('municipios'))
'''Ruta encargada de borrar registros de municipios'''
@app.route('/municipio/borrar/<string:cod_municipio>', methods=['GET','POST'])
def borrarmunicipio(cod_municipio):
    '''Funcion encargada de borrar registros de la tabla municipios'''
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM municipios WHERE cod_municipio={0}'.format(cod_municipio))
    mysql.connection.commit()
    flash('Registro Eliminado')
    return redirect(url_for('municipios'))




'''Ruta para los manzanas'''
@app.route ('/manzanas',methods=['GET','POST'])
def manzana():
    '''Se establece la función para la ruta para la seccion municipios'''
    cur=mysql.connection.cursor()
    cur.execute('SELECT cod_manzana,nombre_municipio,nombre_manzana,localidad,direccion_manzana,nombre_servicio FROM manzanas,municipios,servicios,appleservice WHERE manzanas.cod_municipio=municipios.cod_municipio AND manzanas.cod_manzana=appleservice.copy_codmanzana AND servicios.cod_servicio=appleservice.copy_codservice')
    info=cur.fetchall()

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
    return render_template('Admin/manzanas.html', manzanas=info)#Devolvera el template manzana.html
@app.route('/manzanas/edit/<cod_manzanas>', methods=['POST', 'GET'])
def get_manzanas(cod_manzanas):
    cur=mysql.connection.cursor()
    cur.execute('SELECT cod_manzana,manzanas.cod_municipio,nombre_manzana,localidad,direccion_manzana,nombre_servicio FROM manzanas,municipios,servicios,appleservice WHERE manzanas.cod_municipio=municipios.cod_municipio AND manzanas.cod_manzana=appleservice.copy_codmanzana AND servicios.cod_servicio=appleservice.copy_codservice')
    info=cur.fetchall()
    print(info[0])
    return render_template('edicion/editmanzanas.html',manzanas=info[0])
'''Ruta encargada de editar registros de manzanas'''
@app.route('/manzanas/update/<cod_manzana>',methods=['GET','POST'])
def update_manzanas(cod_manzana):
    
    if request.method=='POST':
        cod = request.form['codmanzana']
        name = request.form['nombres']
        cod2 = request.form['codmunicipio']
        localidad = request.form['localidad']
        direccion = request.form['direccion']
        codserv=request.form['servicioprest']

        cur=mysql.connection.cursor()
        cur.execute('UPDATE manzanas SET cod_manzana=%s,cod_municipio=%s,nombre_manzana=%s,localidad=%s,direccion_manzana=%s WHERE cod_manzana=%s',(cod,cod2,name,localidad,direccion,cod))
        cur.execute('UPDATE appleservice SET copy_codmanzana=%s,copy_codservice=%s WHERE copy_codmanzana=%s',(cod,codserv,cod))

        mysql.connection.commit()
        flash('Manzana Actualizada')
        return redirect(url_for('manzana'))
@app.route('/manzana/borrar/<string:cod_manzana>', methods=['GET','POST'])
def borrarmanzana(cod_manzana):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM appleservice WHERE copy_codmanzana={0}'.format(cod_manzana))
    mysql.connection.commit()
    cur.execute('DELETE FROM manzanas WHERE cod_manzana={0}'.format(cod_manzana))
    mysql.connection.commit()
    flash('Registro Eliminado')
    return redirect(url_for('manzana'))



'''Rutas de Manzanas que se les mostrara a las mujeres en manzanaMujer.html'''
@app.route ('/manzanasMujer',methods=['GET','POST'])
def manzanamujer():
    '''Se establece la función para la ruta para la seccion municipios'''
    cur=mysql.connection.cursor()
    cur.execute('SELECT cod_manzana,nombre_municipio,nombre_manzana,localidad,direccion_manzana,nombre_servicio FROM manzanas,municipios,servicios,appleservice WHERE manzanas.cod_municipio=municipios.cod_municipio AND manzanas.cod_manzana=appleservice.copy_codmanzana AND servicios.cod_servicio=appleservice.copy_codservice')
    info=cur.fetchall()
    return render_template('Mujer/manzanaMujer.html', manzanas=info)#Devolvera el template manzana.html


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

    return render_template('Admin/servicios.html', servicios=info)#Devolvera el template servicios.html ubicado en la carpeta templates/modulos
'''Ruta encargada de capturar la primary key de los resgistros de servicios'''
@app.route('/servicio/edit/<cod_servicio>', methods=['POST', 'GET'])
def get_servicio(cod_servicio):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM servicios WHERE cod_servicio = %s', (cod_servicio))
    data = cur.fetchall()
    cur.close()
    return render_template('edicion/editservicios.html',servicios=data[0])
'''Ruta encargada de editar registros de servicios'''
@app.route('/servicio/update/<cod_servicio>',methods=['GET','POST'])
def update_servicios(cod_servicio):

    if request.method=='POST':
        cod = request.form['codservicio']
        name = request.form['nombres']
        description = request.form['descripcion']

        cur = mysql.connection.cursor()
        cur.execute('UPDATE servicios SET nombre_servicio=%s,descripcion=%s WHERE cod_servicio=%s',(name,description,cod))
        mysql.connection.commit()
        flash('Servicio Actualizado')
        return redirect(url_for('servicios'))
'''Ruta encargada de borrar registros de servicios'''
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

    return render_template('Admin/establecimientos.html',establecimiento=info)#Devolvera el template establecimientos.html
'''Ruta encargada de capturar la primary key de los resgistros de establecimientos'''
@app.route('/establecimientos/edit/<cod_establecimiento>', methods=['POST', 'GET'])
def get_establecimiento(cod_establecimiento):
    cur=mysql.connection.cursor()
    cur.execute('SELECT cod_establecimiento,nombre_establecimiento,responsable,direccion_establecimiento,nombre_servicio FROM establecimiento,servicios WHERE establecimiento.cod_servicio=servicios.cod_servicio')
    info=cur.fetchall()
    return render_template('edicion/editestablecimientos.html',establecimientos=info[0])
'''Ruta encargada de editar registros de establecimientos'''
@app.route('/establecimientos/update/<cod_establecimiento>',methods=['GET','POST'])
def update_establecimientos(cod_establecimiento):
    
    if request.method=='POST':
        cod = request.form['codestablecimiento']
        name = request.form['nombres']
        responsable = request.form['responsable']
        direccion = request.form['direccion']
        service= request.form['service']

        cur=mysql.connection.cursor()
        cur.execute('UPDATE establecimiento SET cod_servicio=%s,nombre_establecimiento=%s,responsable=%s,direccion_establecimiento=%s WHERE cod_establecimiento=%s',(service,name,responsable,direccion,cod))
        mysql.connection.commit()
        flash('Establecimiento Actualizado')
        return redirect(url_for('establecimientos'))
'''Ruta encargada de borrar resgistros de servicios'''
@app.route('/establecimiento/borrar/<string:cod_establecimiento>', methods=['GET','POST'])
def borrarestablecimiento(cod_establecimiento):
    '''Funcion encargada de borrar registros de la tabla establecimientos'''
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM establecimiento WHERE cod_establecimiento={0}'.format(cod_establecimiento))
    mysql.connection.commit()
    flash('Registro Eliminado')
    return redirect(url_for('establecimientos'))




'''Ruta para el registro de las Mujeres pov admin'''
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
        password=request.form['contraseña']
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
                cur.execute('INSERT INTO mujeres(documento,cod_servicio,tipoDocumento,nombres_mujer,apellidos_mujer,telefono,correo,contraseña,ciudad,direccion_mujer,ocupacion) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(doc,servicioint,tipodoc,name,lastname,tel,email,password,city,address,ocupacion))
                mysql.connection.commit()
                flash('Cuidadora Agregada Satisfactoriamente')
        return redirect(url_for('cuidadora'))#SI el registro se completa satisfactoriamente se habilita el mensaje y se redirige al formulario
    
    return render_template('Admin/mujeres.html', mujeres=info)#Devolvera el template mujeres.html
'''Ruta encargada de capturar la primary key de los resgistros de mujeres'''
@app.route('/mujeres/edit/<documento>', methods=['POST', 'GET'])
def get_mujeres(documento):
    cur=mysql.connection.cursor()
    cur.execute('SELECT documento,mujeres.cod_servicio,tipoDocumento,nombres_mujer,apellidos_mujer,telefono,correo,ciudad,direccion_mujer,ocupacion FROM mujeres,servicios WHERE mujeres.cod_servicio=servicios.cod_servicio')
    info=cur.fetchall()
    cur.close()
    return render_template('edicion/editmujeres.html',mujeres=info[0])
'''Ruta encargada de editar registros de mujeres'''
@app.route('/mujeres/update/<documento>',methods=['GET','POST'])
def update_mujeres(documento):

    if request.method=='POST':
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

        cur = mysql.connection.cursor()
        cur.execute('UPDATE mujeres SET cod_servicio=%s,tipoDocumento=%s,nombres_mujer=%s,apellidos_mujer=%s,telefono=%s,correo=%s,ciudad=%s,direccion_mujer=%s,ocupacion=%s WHERE documento=%s',(servicioint,tipodoc,name,lastname,tel,email,city,address,ocupacion,doc))
        mysql.connection.commit()

        
        flash('Mujer Actualizada')
        return redirect(url_for('cuidadora'))
'''Ruta encargada de eliminar los resgistros de mujeres'''
@app.route('/mujer/borrar/<string:documento>', methods=['GET','POST'])
def borrarmujer(documento):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM mujeres WHERE documento={0}'.format(documento))
    mysql.connection.commit()
    flash('Registro Eliminado')
    return redirect(url_for('cuidadora'))
'''Registro de mujeres pov usuarias'''
@app.route('/registromujer',methods=('GET','POST'))
def registromujer():

    return render_template('registromujer.html')


'''Ruta para la asignación'''
@app.route ('/asignacion', methods=['GET','POST'])
def asignacion():
    '''Se establece la función para la ruta para la seccion asignación'''
    cur=mysql.connection.cursor()
    cur.execute('SELECT documento_mujer,nombres_mujer,apellidos_mujer,nombre_manzana,nombre_servicio,fecha,hora FROM cuidadoras,mujeres,servicios,manzanas WHERE cuidadoras.documento_mujer=mujeres.documento AND cuidadoras.cod_manzana=manzanas.cod_manzana AND cuidadoras.cod_servicio=servicios.cod_servicio')
    info=cur.fetchall()

    if request.method == 'POST':
        documento = request.form['documento']
        cod1 = request.form['codmanzana']
        cod2 = request.form['service']
        date = request.form['dia']
        time = request.form['hora']

        cur.execute('SELECT * FROM cuidadoras WHERE documento_mujer=%s',[documento,])#Se verifica que el establecimiento no haya sido previamente ingresado
        data=cur.fetchone()

        if data:
            flash('Ya cuenta con una cita asignada')
            return redirect(url_for('establecimientos'))#Si el servicio se encuentra ya resgistrao se habilita el mensaje de aviso y se redirije al formulario

        else:
            cur.execute('INSERT INTO cuidadoras(documento_mujer,cod_manzana,cod_servicio,fecha,hora) VALUES(%s,%s,%s,%s,%s)',(documento,cod1,cod2,date,time))
            mysql.connection.commit()
            flash('Cita Asignada')
            return redirect(url_for('asignacion'))
    return render_template('Admin/asignacion.html', cuidadoras=info)#Devolvera el template asignacion.html
'''Ruta encargada de capturar la primary key de los resgistros de asignaciones'''
@app.route('/asignacion/edit/<documento_mujer>', methods=['POST', 'GET'])
def get_asignacion(documento_mujer):
    cur=mysql.connection.cursor()
    cur.execute('SELECT documento_mujer,cuidadoras.cod_manzana,nombre_servicio,fecha,hora FROM cuidadoras,mujeres,servicios,manzanas WHERE cuidadoras.documento_mujer=mujeres.documento AND cuidadoras.cod_manzana=manzanas.cod_manzana AND cuidadoras.cod_servicio=servicios.cod_servicio')
    info=cur.fetchall()
    return render_template('edicion/editasignaciones.html',cuidadoras=info[0])
'''Ruta encargada de editar registros de asignaciones'''
@app.route('/asignacion/update/<documento_mujer>',methods=['GET','POST'])
def update_asignaciones(documento_mujer):
    if request.method=='POST':
        documento= request.form['documento']
        cod1 = request.form['codmanzana']
        cod2 = request.form['service']
        date = request.form['dia']
        time = request.form['hora']

        cur=mysql.connection.cursor()
        cur.execute('UPDATE cuidadoras SET cod_manzana=%s,cod_servicio=%s,fecha=%s,hora=%s WHERE documento_mujer=%s',(cod1,cod2,date,time,documento))
        mysql.connection.commit()
        flash('Cita Re-asignada')
        return redirect(url_for('asignacion'))
'''Ruta encargada de eliminar registros de asignaciones'''
@app.route('/asignacion/borrar/<string:documento_mujer>', methods=['GET','POST'])
def borrarasignacion(documento_mujer):
    '''Funcion encargada de borrar registros de la tabla municipios'''
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM cuidadoras WHERE documento_mujer={0}'.format(documento_mujer))
    mysql.connection.commit()
    flash('Registro Eliminado')
    return redirect(url_for('asignacion'))


'''Rutas de asignaciones que se les mostrará a las mujeres en asignacionMujer.html'''
@app.route ('/vista', methods=['GET','POST'])
def asignacionmujer():
    '''Se establece la función para la ruta para la seccion asignación'''
    cur=mysql.connection.cursor()
    cur.execute('SELECT documento_mujer,nombres_mujer,apellidos_mujer,nombre_manzana,nombre_servicio,fecha,hora FROM cuidadoras,mujeres,servicios,manzanas WHERE cuidadoras.documento_mujer=mujeres.documento AND cuidadoras.cod_manzana=manzanas.cod_manzana AND cuidadoras.cod_servicio=servicios.cod_servicio')
    info=cur.fetchall()

    if request.method == 'POST':
        documento = request.form['documento']
        cod1 = request.form['codmanzana']
        cod2 = request.form['service']
        date = request.form['dia']
        time = request.form['hora']

        cur.execute('SELECT * FROM cuidadoras WHERE documento_mujer=%s',[documento,])#Se verifica que el establecimiento no haya sido previamente ingresado
        data=cur.fetchone()

        if data:
            flash('Ya cuenta con una cita asignada')
            return redirect(url_for('asignacionmujer'))#Si el servicio se encuentra ya resgistrada se habilita el mensaje de aviso y se redirije al formulario
    return render_template('Mujer/asignacionMujer.html', cuidadoras=info)
'''Boton eliminacion en vista asignacionMujer'''
@app.route('/asignacionMujer/borrar/<string:documento_mujer>', methods=['GET','POST'])
def borrarasignacionmujer(documento_mujer):
    '''Funcion encargada de borrar registros de la tabla municipios'''
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM cuidadoras WHERE documento_mujer={0}'.format(documento_mujer))
    mysql.connection.commit()
    flash('Registro Eliminado')
    return redirect(url_for('asignacionmujer'))

'''Ruta para los reportes'''
@app.route ('/reportes')
def reporte():
    report=reportes()
    return report
def pdf_report(data):
    '''crear el reporte con el boton en el html'''
    # Crear el PDF usando reportlab
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # Agregar contenido al PDF
    y = 700  # Posición inicial en y para el primer dato
    for row in data:
        x = 80  # Posición en x para el primer dato
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



'''Rutas de los modulos en (botones) PDF'''
'''Genera el pdf en el modulo municipios'''
@app.route('/generar_pdf', methods=['GET','POST']) #Genera el pdf de municipios
def generarpdf():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM municipios')
    data=cur.fetchall()

    pdf = pdf_report(data)

    response = make_response(pdf)
    response.headers['Content-Disposition'] = 'attachment; filename=Reporte Municipios.pdf'
    response.mimetype = 'application/pdf'
    return response
'''Genera el pdf en el modulo asignaciones'''
@app.route('/generar_pdfC', methods=['GET','POST']) #Genera el PDF de las Asignaciones
def generarpdfC():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM cuidadoras')
    data=cur.fetchall()

    pdf = pdf_report(data)

    response = make_response(pdf)
    response.headers['Content-Disposition'] = 'attachment; filename=Reporte Asignaciones.pdf'
    response.mimetype = 'application/pdf'
    return response
'''Genera el pdf en el modulo manzanas'''
@app.route('/generar_pdfM', methods=['GET','POST']) #Genera el PDF de las Manzanas
def generarpdfM():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM manzanas')
    data=cur.fetchall()

    pdf = pdf_report(data)

    response = make_response(pdf)
    response.headers['Content-Disposition'] = 'attachment; filename=Reporte Manzanas.pdf'
    response.mimetype = 'application/pdf'
    return response
'''Genera el pdf en el modulo servicios'''
@app.route('/generar_pdfS', methods=['GET','POST']) #Genera el PDF de las servicios
def generarpdfS():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM servicios')
    data=cur.fetchall()

    pdf = pdf_report(data)

    response = make_response(pdf)
    response.headers['Content-Disposition'] = 'attachment; filename=Reporte Servicios.pdf'
    response.mimetype = 'application/pdf'
    return response
'''Genera el pdf en el modulo Mujeres'''
@app.route('/generar_pdfW', methods=['GET','POST']) #Genera el PDF de las Mujeres
def generarpdfW():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM mujeres')
    data=cur.fetchall()

    pdf = pdf_report(data)

    response = make_response(pdf)
    response.headers['Content-Disposition'] = 'attachment; filename=Reporte Mujeres.pdf'
    response.mimetype = 'application/pdf'
    return response
'''Genera el pdf en el modulo Establecimientos'''
@app.route('/generar_pdfE', methods=['GET','POST']) #Genera el PDF de las Establecimientos
def generarpdfE():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM establecimiento')
    data=cur.fetchall()

    pdf = pdf_report(data)

    response = make_response(pdf)
    response.headers['Content-Disposition'] = 'attachment; filename=Establecimientos.pdf'
    response.mimetype = 'application/pdf'
    return response




if __name__=='__main__':
    #Se verifica que se este corriendo la aplicacion.
    app.run(debug=True)
