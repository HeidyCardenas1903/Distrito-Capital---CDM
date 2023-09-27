'''Modulo dedicado a todas las funciones de los distintos modulos de la app'''

from flask import Flask, render_template, request, redirect,url_for,flash,session
 

def manzanas():
    '''Se establece la función para la ruta para la seccion manzanas'''
    return render_template('modulos/manzanas.html')#Devolvera el template manzana.html

def servicios():
    '''Se establece la función para la ruta para la seccion servicios'''
    return render_template('modulos/servicios.html')#Devolvera el template manzana.html

def establecimientos():
    '''Se establece la función para la ruta para la seccion establecimientos'''
    return render_template('modulos/establecimientos.html')#Devolvera el template establecimientos.html

def asignacion():
    '''Se establece la función para la ruta para la seccion asignación'''
    return render_template('modulos/asignacion.html')#Devolvera el template asignacion.html

def reportes():
    '''Se establece la función para la ruta para la seccion reportes'''
    return render_template('modulos/reportes.html')#Devolvera el template reportes.html