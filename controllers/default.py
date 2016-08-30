# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from gluon.tools import Crud
crud = Crud(db)

from datetime import date, timedelta

 #from datetime import time, timedelta

import datetime
import string
#import yaml


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Hello World")
    #return dict(message=T('Welcome to web2py!'))
    return dict()

def inicio():
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def calendar2():
    paciente_id=request.args(0)
    paciente=db.paciente[paciente_id]
    if paciente_id:
       tasks=db(db.task.paciente==paciente_id)\
               (db.task.created_by==auth.user.id)\
               (db.task.start_time>=request.now).select()
    else:
       tasks=db(db.task.created_by==auth.user.id)\
               (db.task.start_time>=request.now).select()
    return dict(tasks=tasks,paciente=paciente)

#pagina principal despues del login
@auth.requires_login()
def calendar():
    #tasks=db(db.task).select()
    #registros=db().select(
    #    db.paciente.ALL, db.task.ALL,
    #    left = db.paciente.on(db.paciente.id==db.task.paciente)&(db.task.created_by==1))
    registros= db((db.paciente.id==db.task.paciente)&
        (db.task.created_by==auth.user.id)).select()
    return dict(registros=registros)
    #tasks=db(db.task.start_time>=request.now).select()

#agrego un nuevo paciente
@auth.requires_login()
def abmPacientes():
    #grid = SQLFORM.grid(db.paciente,field_id=None)
    return dict(formulario=crud.create(db.paciente,next='getAllPacientes',fields=['nombres','apellidos','dni','fechaNac','obraSocial','domicilio','telFijo','celular','email'],message='Paciente Registrado con Exito'))
    return locals()

#devuelve todos los pacientes de la bd
@auth.requires_login()
def getAllPacientes():
    registros=db().select(
        db.paciente.ALL, db.obraSocial.ALL,
        left = db.obraSocial.on(db.paciente.obraSocial==db.obraSocial.id))
    return dict(registros=registros)
    #pacientes = db(db.paciente).select()
    #turnosDelDia = db(db.task.start_time==request.now).select()
    #return dict(pacientes=pacientes)
@auth.requires_login()
@service.json
def getAllPacientesAjax2():
    registros=db().select(
        db.paciente.ALL, db.obraSocial.ALL,
        left = db.obraSocial.on(db.paciente.obraSocial==db.obraSocial.id))
    #return dict(registros=registros)
    return response.json(registros)

def getAllPacientesAjax():
    response.view='default/getAllPacientesAjax.html'
    return dict(message=T("Hello World"))


def allPacientes():
    pacientes = db(db.paciente).select()
    #turnosDelDia = db(db.task.start_time==request.now).select()
    return dict(pacientes=pacientes)

@auth.requires_login()
def editarPaciente():
    #id = ((request.args(0)) or redirect(URL('calendar'))
    return dict(formulario=crud.update(db.paciente,(request.args(0)),next='getAllPacientes',fields=['nombres','apellidos','dni','fechaNac','obraSocial','domicilio','telFijo','celular','email'],message='Registro editado con Exito'))
    #crud.update(db.nombredelatabla, id)

#devuelve todos los turnos del paciente ordenador por fecha desc NECESITA EL ID DEL PACIENTE
@auth.requires_login()
def turnosDelPaciente():
    paciente_id=request.args(0)
    paciente = db.paciente(request.args(0))    
    if paciente_id:
       #turnos=db(db.task.paciente==paciente_id, orderby=~db.task.start_time)
       #turnos=db().select(db.task.paciente==paciente_id)

       #registros=db().select(
       #db.auth_user.ALL, db.task.ALL,
       #left = db.auth_user.on(db.paciente.id==db.task.paciente))
       # return dict(registros=registros)

       turnos=db(db.task.paciente==paciente_id).select(orderby=~db.task.start_time)

       #turnos=db(db.task.paciente==paciente_id)
       #turnos = db.executesql('SELECT * FROM task where task.id=;')
       return dict(paciente=paciente,turnos=turnos)
       #return dict(paciente=paciente,registros=registros)

@auth.requires_login()
def concluirTurno():
    idpaciente = (request.args(1))
    idturno = (request.args(0))
    turno = db(db.task.id == idturno).select().first()
    if (turno.concluido ):
        resultado = db(db.task.id == idturno).update(concluido=False)
    else:
        resultado = db(db.task.id == idturno).update(concluido=True)
    session.flash = 'Turno Actualizado con exito'    
    return redirect(URL('turnosDelPaciente', args=(idpaciente)))

@auth.requires_login()
def eliminarTurno():
    idpaciente = (request.args(1))
    idturno = (request.args(0))
    resultado = db(db.task.id == idturno).delete()
    session.flash = 'Turno eliminado con exito'    
    return redirect(URL('turnosDelPaciente', args=(idpaciente)))    
    
    #return dict(formulario=crud.delete(db.task, request.args(0),next='getAllPacientes',message='Registro eliminado con Exito'))
    #return locals()

@auth.requires_login()
def editarTurnoCalendar():
    idpaciente =(request.args(1))
    #siguiente = crud.settings.update_next = URL('turnosDelPaciente', args=(idpaciente))
    encabezado = {'start_time': 'Fecha y Hora'}
    return dict(formulario=crud.update(db.task,(request.args(0)),fields=['start_time','stop_time','description','nro_sesion','concluido'],next='calendar',headers=encabezado,message='Registro editado con Exito'))

#editar turno del paciente
@auth.requires_login()
def editarTurno():
    idpaciente =(request.args(1))
    siguiente = crud.settings.update_next = URL('turnosDelPaciente', args=(idpaciente))
    return dict(formulario=crud.update(db.task,(request.args(0)),fields=['title','start_time','stop_time','description','nro_sesion','concluido'],next=siguiente,message='Registro editado con Exito'))
    #redirect(URL('turnosDelPaciente', args=(idpaciente)))
    #return locals()
    #crud.update(db.nombredelatabla, id)

@auth.requires_login()
def crearTurno():
    "lists all documents attached to a certain page"
    paciente = db.paciente(request.args(0)) or redirect(URL('calendar'))
    db.task.paciente.default = paciente.id
    form = crud.create(db.task)
    #pagedocuments = db(db.document.page_id==this_page.id).select()
    return dict(form=form)

#funcion que devuelve un formulario para crear turnos recibe como parametro el id del paciente
@auth.requires_login()
def turno_formulario():
    paciente = db.paciente(request.args(0)) or redirect(URL('calendar'))
    #hoy=datetime.datetime.now()-timedelta(days=0)
    #manana=date.today()+timedelta(days=1)
    # 0 es equivalente a domingo y 6 equivale a sabado
    #dia =  hoy.strftime('%w')
    #return dict(paciente=paciente,hoy=hoy,manana=manana,dia=dia)
    return dict(paciente=paciente)

#funcion que registra los turnos nuevos
@auth.requires_login()
def agregarTurno():
    paciente_id = request.vars['id']    
    nro_sesion = int(request.vars['nro_sesion'])
    duration = int(request.vars['duracion'])
    #nro = int(request.vars['nro_sesion'])
    nro = 1
    fecha1 = datetime.datetime.strptime(request.vars['start_time'], "%Y-%m-%dT%H:%M")
    dia =  fecha1.strftime('%w')
    dia = int(dia)
    #print request.vars['nro_sesion']
    valor = 1
    rango = nro_sesion
    if (dia == 0 or dia == 6):
        session.flash = 'La fecha ingresada es incorrecta ya que es Sabado o Domingo'        
        redirect(URL('turno_formulario', args=(paciente_id))) 
        #response.flash = 'La fecha ingresada es incorrecta ya que es Sabado o Domingo'
    else:
        while valor <= rango:          
            dia2 =  fecha1.strftime('%w')
            dia2 = int(dia2)
            if (dia2 == 0 or dia2 == 6):
                fecha1=fecha1+timedelta(days=1)
                #valor = valor - 1
            else:
                id = db.task.insert(title="Turno",description=request.vars['description'],duracion=duration,nro_sesion=nro,
                start_time=fecha1,stop_time=fecha1+ timedelta(minutes=duration),paciente=request.vars['id'])
                fecha1=fecha1+timedelta(days=1)
                nro += 1  
                valor = valor + 1
    #     #id=db(db.task.paciente==request.vars['paciente']).select()
        session.flash = 'Turno/s registrado/s con éxito'
        redirect(URL('turnosDelPaciente', args=(paciente_id)))   
    # if dia == 0:
    #     response.flash = 'La fecha ingresada es incorrecta ya que es Sabado o Domingo'
    #     redirect(URL('turno_formulario', vars=dict(id=request.vars['id']))) 
    # else:        
    #     id = db.task.insert(title="Turno",description=request.vars['description'],nro_sesion=request.vars['nro_sesion'],
    #         start_time=fecha1,stop_time=fecha1,paciente=request.vars['id'])
    #     #id=db(db.task.paciente==request.vars['paciente']).select()
    #     response.flash = 'Turno registrado con éxito'
    #     return dict(formulario=crud.read(db.task,id))

@auth.requires_login()
def agregarTurno2():
    #print request.vars['id']
    print request.vars['description']     


#        Field('title','string'),
#    Field('task_type'),
#    Field('paciente',db.paciente),
#    Field('description','text'),
#    Field('start_time','datetime'),
#    Field('stop_time','datetime'),
#    Field('nro_sesion','integer',default=1),
#    Field('concluido','boolean',default=False),
#    Field('created_by',db.auth_user,default=auth.user_id,writable=False,readable=False),
#    Field('created_on','datetime',default=request.now,writable=False,readable=False)
